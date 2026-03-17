#!/usr/bin/env tsx
/**
 * OpenClaw 集成钩子
 * 
 * 自动挂钩到 OpenClaw 会话流
 * 
 * 用法：
 *   在 OpenClaw 配置中启用：
 *   {
 *     "evolution": {
 *       "enabled": true,
 *       "autoCollect": true,
 *       "autoReflect": "daily"
 *     }
 *   }
 */

import { appendFile, readFile, writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// ============================================================
// 配置
// ============================================================

const WORKSPACE_DIR = join(process.env.HOME || '~', '.openclaw/workspace');
const EVOLUTION_DIR = join(WORKSPACE_DIR, 'memory/evolution');
const SESSION_LOG = join(EVOLUTION_DIR, 'sessions.jsonl');
const CONFIG_FILE = join(WORKSPACE_DIR, 'evolution-config.json');

// ============================================================
// 类型定义
// ============================================================

export interface SessionData {
  session_id: string;
  chat_id: string;
  started_at: string;
  ended_at?: string;
  success: boolean;
  task?: string;
  input?: string;
  output?: string;
  error?: string;
  duration_ms?: number;
  tokens_used?: number;
  model?: string;
  tools_called?: string[];
  user_feedback?: 'positive' | 'negative' | 'neutral';
}

export interface EvolutionConfig {
  enabled: boolean;
  autoCollect: boolean;
  autoReflect: 'disabled' | 'daily' | 'weekly';
  reflectTime: string; // cron 格式，如 "0 3 * * *"
  maxEvents: number;
  injectContext: boolean;
}

// ============================================================
// 配置管理
// ============================================================

export async function loadConfig(): Promise<EvolutionConfig> {
  const defaultConfig: EvolutionConfig = {
    enabled: true,
    autoCollect: true,
    autoReflect: 'daily',
    reflectTime: '0 3 * * *',
    maxEvents: 10000,
    injectContext: true,
  };
  
  if (!existsSync(CONFIG_FILE)) {
    await saveConfig(defaultConfig);
    return defaultConfig;
  }
  
  return {
    ...defaultConfig,
    ...JSON.parse(await readFile(CONFIG_FILE, 'utf-8')),
  };
}

export async function saveConfig(config: EvolutionConfig): Promise<void> {
  await mkdir(EVOLUTION_DIR, { recursive: true });
  await writeFile(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

// ============================================================
// 会话钩子
// ============================================================

/**
 * 会话开始时调用
 * 注入历史上下文到 prompt
 */
export async function onSessionStart(sessionId: string, chatId: string): Promise<string> {
  const config = await loadConfig();
  
  if (!config.enabled || !config.injectContext) {
    return '';
  }
  
  try {
    // 调用上下文注入器
    const { loadFullContext } = await import('./context-injector.js');
    const context = await loadFullContext();
    
    // 记录会话开始
    await logSessionStart(sessionId, chatId);
    
    return context;
  } catch (error) {
    console.error('[Evolution] Session start hook error:', error);
    return '';
  }
}

/**
 * 会话结束时调用
 * 自动收集事件
 */
export async function onSessionEnd(
  sessionId: string,
  data: {
    success: boolean;
    task?: string;
    input?: string;
    output?: string;
    error?: string;
    duration_ms?: number;
    tokens_used?: number;
    model?: string;
    tools_called?: string[];
  }
): Promise<void> {
  const config = await loadConfig();
  
  if (!config.enabled || !config.autoCollect) {
    return;
  }
  
  try {
    // 记录会话结束
    await logSessionEnd(sessionId, data);
    
    // 自动收集事件
    const { collectEvent } = await import('./event-collector.js');
    
    const eventType = data.success ? 'success' : 'failure';
    await collectEvent({
      event_type: eventType,
      session_id: sessionId,
      task: data.task,
      input: data.input,
      output: data.output,
      error: data.error,
      meta: {
        duration_ms: data.duration_ms,
        tokens_used: data.tokens_used,
        model: data.model,
        tools_called: data.tools_called,
      },
    });
    
    console.log(`[Evolution] Auto-collected ${eventType} event for session ${sessionId}`);
  } catch (error) {
    console.error('[Evolution] Session end hook error:', error);
  }
}

/**
 * 用户纠正时调用
 */
export async function onUserCorrection(
  sessionId: string,
  correction: {
    what: string;
    corrected: string;
    original?: string;
  }
): Promise<void> {
  const config = await loadConfig();
  
  if (!config.enabled || !config.autoCollect) {
    return;
  }
  
  try {
    const { collectEvent } = await import('./event-collector.js');
    
    await collectEvent({
      event_type: 'correction',
      session_id: sessionId,
      what: correction.what,
      correction: correction.corrected,
      meta: {
        original: correction.original,
      },
    });
    
    console.log(`[Evolution] Auto-collected correction event for session ${sessionId}`);
  } catch (error) {
    console.error('[Evolution] Correction hook error:', error);
  }
}

// ============================================================
// 会话日志
// ============================================================

async function logSessionStart(sessionId: string, chatId: string): Promise<void> {
  const logEntry = {
    event: 'session_start',
    session_id: sessionId,
    chat_id: chatId,
    timestamp: new Date().toISOString(),
  };
  
  await appendFile(SESSION_LOG, JSON.stringify(logEntry) + '\n', 'utf-8');
}

async function logSessionEnd(sessionId: string, data: any): Promise<void> {
  const logEntry = {
    event: 'session_end',
    session_id: sessionId,
    timestamp: new Date().toISOString(),
    ...data,
  };
  
  await appendFile(SESSION_LOG, JSON.stringify(logEntry) + '\n', 'utf-8');
}

// ============================================================
// 自动反思调度
// ============================================================

export async function setupAutoReflect(): Promise<void> {
  const config = await loadConfig();
  
  if (config.autoReflect === 'disabled') {
    // 清除 cron 任务
    await removeCronJob();
    return;
  }
  
  // 添加 cron 任务
  const cronExpr = config.reflectTime;
  const reflectScript = join(WORKSPACE_DIR, 'skills/evolution-engine-v2/src/reflector.ts');
  const cronJob = `${cronExpr} cd ${WORKSPACE_DIR} && npx tsx ${reflectScript} >> ${EVOLUTION_DIR}/reflect.log 2>&1`;
  
  await addCronJob(cronJob);
  console.log(`[Evolution] Auto-reflect scheduled: ${cronExpr}`);
}

async function addCronJob(job: string): Promise<void> {
  try {
    // 获取当前 crontab
    const { stdout: current } = await execAsync('crontab -l 2>/dev/null || echo ""');
    
    // 检查是否已存在
    if (current.includes('evolution-engine-v2/src/reflector.ts')) {
      console.log('[Evolution] Cron job already exists');
      return;
    }
    
    // 添加新任务
    const newCrontab = current.trim() + '\n' + job + '\n';
    
    // 写入 crontab
    const tmpFile = `/tmp/crontab_${Date.now()}`;
    await writeFile(tmpFile, newCrontab);
    await execAsync(`crontab ${tmpFile}`);
    await execAsync(`rm ${tmpFile}`);
    
    console.log('[Evolution] Cron job added');
  } catch (error) {
    console.error('[Evolution] Failed to add cron job:', error);
  }
}

async function removeCronJob(): Promise<void> {
  try {
    const { stdout: current } = await execAsync('crontab -l 2>/dev/null || echo ""');
    
    // 移除进化引擎相关任务
    const newCrontab = current
      .split('\n')
      .filter(line => !line.includes('evolution-engine-v2/src/reflector.ts'))
      .join('\n');
    
    if (newCrontab.trim()) {
      const tmpFile = `/tmp/crontab_${Date.now()}`;
      await writeFile(tmpFile, newCrontab);
      await execAsync(`crontab ${tmpFile}`);
      await execAsync(`rm ${tmpFile}`);
    } else {
      await execAsync('crontab -r 2>/dev/null || true');
    }
    
    console.log('[Evolution] Cron job removed');
  } catch (error) {
    console.error('[Evolution] Failed to remove cron job:', error);
  }
}

// ============================================================
// CLI 命令
// ============================================================

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'init':
      const config = await loadConfig();
      console.log('🧬 Evolution Engine v2 配置:');
      console.log(JSON.stringify(config, null, 2));
      await setupAutoReflect();
      break;
      
    case 'enable':
      const enableConfig = await loadConfig();
      enableConfig.enabled = true;
      await saveConfig(enableConfig);
      await setupAutoReflect();
      console.log('✅ Evolution Engine 已启用');
      break;
      
    case 'disable':
      const disableConfig = await loadConfig();
      disableConfig.enabled = false;
      await saveConfig(disableConfig);
      await removeCronJob();
      console.log('⏸️ Evolution Engine 已禁用');
      break;
      
    case 'status':
      const statusConfig = await loadConfig();
      console.log('📊 Evolution Engine 状态:');
      console.log(`  启用：${statusConfig.enabled}`);
      console.log(`  自动收集：${statusConfig.autoCollect}`);
      console.log(`  自动反思：${statusConfig.autoReflect}`);
      console.log(`  反思时间：${statusConfig.reflectTime}`);
      console.log(`  注入上下文：${statusConfig.injectContext}`);
      break;
      
    default:
      console.log(`
🧬 OpenClaw Evolution Engine v2 - 集成钩子

用法:
  tsx openclaw-integration.ts init      # 初始化配置
  tsx openclaw-integration.ts enable    # 启用
  tsx openclaw-integration.ts disable   # 禁用
  tsx openclaw-integration.ts status    # 查看状态

在 OpenClaw 中集成:
  1. 在 agent 运行时中调用 onSessionStart() 和 onSessionEnd()
  2. 或在 openclaw.json 中配置自动钩子
`);
  }
}

// CLI 入口
const isMainModule = import.meta.url === `file://${process.argv[1]}`;
if (isMainModule) {
  main().catch(console.error);
}
