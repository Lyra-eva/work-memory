#!/usr/bin/env tsx
/**
 * 进化事件收集器 v2
 * 
 * OpenClaw 原生版本 - 自动挂钩到会话流
 * 
 * 用法：
 *   1. 手动：tsx event-collector.ts collect --type <type> --data <json>
 *   2. 自动：在 OpenClaw 会话结束后自动调用
 */

import { appendFile, readFile, writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { randomBytes } from 'crypto';

// ============================================================
// 类型定义
// ============================================================

export type EventType = 'success' | 'failure' | 'lesson' | 'pattern' | 'capability' | 'correction';

export interface EvolutionEvent {
  event_id: string;
  event_type: EventType;
  timestamp: string;
  session_id?: string;
  chat_id?: string;
  task?: string;
  input?: string;
  output?: string;
  feedback?: string;
  error?: string;
  correction?: string;
  learned?: string;
  confidence?: number;
  importance?: number;
  tags?: string[];
  meta?: {
    model?: string;
    duration_ms?: number;
    tokens_used?: number;
    tools_called?: string[];
    [key: string]: any;
  };
}

export interface EventIndex {
  total_events: number;
  events: Array<{
    event_id: string;
    event_type: EventType;
    timestamp: string;
  }>;
  last_updated: string;
}

// ============================================================
// 配置
// ============================================================

const WORKSPACE_DIR = join(process.env.HOME || '~', '.openclaw/workspace');
const EVOLUTION_DIR = join(WORKSPACE_DIR, 'memory/evolution');
const EVENTS_FILE = join(EVOLUTION_DIR, 'events.jsonl');
const INDEX_FILE = join(EVOLUTION_DIR, 'index.json');

const MAX_EVENTS = 10000;
const MAX_INDEX_SIZE = 100;

// ============================================================
// 核心功能
// ============================================================

async function ensureDir(): Promise<void> {
  if (!existsSync(EVOLUTION_DIR)) {
    await mkdir(EVOLUTION_DIR, { recursive: true });
  }
  if (!existsSync(EVENTS_FILE)) {
    await writeFile(EVENTS_FILE, '', 'utf-8');
  }
}

async function loadIndex(): Promise<EventIndex> {
  if (!existsSync(INDEX_FILE)) {
    return {
      total_events: 0,
      events: [],
      last_updated: new Date().toISOString(),
    };
  }
  return JSON.parse(await readFile(INDEX_FILE, 'utf-8'));
}

async function saveIndex(index: EventIndex): Promise<void> {
  index.last_updated = new Date().toISOString();
  await writeFile(INDEX_FILE, JSON.stringify(index, null, 2), 'utf-8');
}

function generateEventId(): string {
  return `evt_${Date.now()}_${randomBytes(4).toString('hex')}`;
}

export async function collectEvent(event: Omit<EvolutionEvent, 'event_id' | 'timestamp'>): Promise<EvolutionEvent> {
  await ensureDir();
  
  const fullEvent: EvolutionEvent = {
    event_id: generateEventId(),
    timestamp: new Date().toISOString(),
    ...event,
    importance: event.importance || 0.5,
    confidence: event.confidence || 0.5,
    tags: event.tags || [],
    meta: event.meta || {},
  };
  
  // 追加到事件文件
  const line = JSON.stringify(fullEvent) + '\n';
  await appendFile(EVENTS_FILE, line, 'utf-8');
  
  // 更新索引
  const index = await loadIndex();
  index.total_events++;
  index.events.push({
    event_id: fullEvent.event_id,
    event_type: fullEvent.event_type,
    timestamp: fullEvent.timestamp,
  });
  
  // 限制索引大小
  if (index.events.length > MAX_INDEX_SIZE) {
    index.events = index.events.slice(-MAX_INDEX_SIZE);
  }
  await saveIndex(index);
  
  // 限制事件文件大小
  await trimEventsFile();
  
  return fullEvent;
}

async function trimEventsFile(): Promise<void> {
  if (!existsSync(EVENTS_FILE)) return;
  
  const content = await readFile(EVENTS_FILE, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim());
  
  if (lines.length > MAX_EVENTS) {
    const trimmed = lines.slice(-MAX_EVENTS);
    await writeFile(EVENTS_FILE, trimmed.join('\n') + '\n', 'utf-8');
  }
}

export async function loadEvents(limit?: number): Promise<EvolutionEvent[]> {
  if (!existsSync(EVENTS_FILE)) {
    return [];
  }
  
  const content = await readFile(EVENTS_FILE, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim());
  
  const events: EvolutionEvent[] = [];
  for (const line of lines) {
    try {
      events.push(JSON.parse(line));
    } catch {
      // 跳过无效行
    }
  }
  
  // 按时间倒序
  events.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  
  if (limit) {
    return events.slice(0, limit);
  }
  
  return events;
}

export async function getStats(): Promise<{
  total: number;
  byType: Record<EventType, number>;
  recent: EvolutionEvent[];
}> {
  const index = await loadIndex();
  const events = await loadEvents(100);
  
  const byType: Record<EventType, number> = {
    success: 0,
    failure: 0,
    lesson: 0,
    pattern: 0,
    capability: 0,
    correction: 0,
  };
  
  for (const event of events) {
    byType[event.event_type] = (byType[event.event_type] || 0) + 1;
  }
  
  return {
    total: index.total_events,
    byType,
    recent: events.slice(0, 10),
  };
}

// ============================================================
// CLI 接口
// ============================================================

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
🧬 进化事件收集器 v2

用法:
  tsx event-collector.ts collect --type <type> --data <json>
  tsx event-collector.ts stats
  tsx event-collector.ts list [--limit <n>]

事件类型:
  success     - 成功事件
  failure     - 失败事件
  lesson      - 经验教训
  pattern     - 发现模式
  capability  - 新能力
  correction  - 用户纠正

示例:
  tsx event-collector.ts collect --type success --data '{"task":"回答问题"}'
  tsx event-collector.ts collect --type failure --data '{"task":"浏览器","error":"timeout"}'
  tsx event-collector.ts collect --type correction --data '{"what":"时区错误","corrected":"Asia/Shanghai"}'
  tsx event-collector.ts stats
`);
    process.exit(0);
  }
  
  const [command, ...rest] = args;
  
  try {
    if (command === 'collect') {
      const typeIdx = rest.indexOf('--type');
      const dataIdx = rest.indexOf('--data');
      const sessionIdx = rest.indexOf('--session');
      
      if (typeIdx === -1 || dataIdx === -1) {
        console.error('❌ 缺少必需参数：--type 和 --data');
        process.exit(1);
      }
      
      const eventType = rest[typeIdx + 1] as EventType;
      const data = JSON.parse(rest[dataIdx + 1]);
      const sessionId = sessionIdx !== -1 ? rest[sessionIdx + 1] : undefined;
      
      const event = await collectEvent({
        event_type: eventType,
        session_id: sessionId,
        ...data,
      });
      
      console.log(`✅ 事件已记录：${event.event_type} [${event.event_id}]`);
      
      const stats = await getStats();
      console.log(`📊 当前总事件数：${stats.total}`);
      
    } else if (command === 'stats') {
      const stats = await getStats();
      console.log('📊 进化事件统计');
      console.log('='.repeat(40));
      console.log(`总事件数：${stats.total}`);
      console.log('\n按类型分布:');
      for (const [type, count] of Object.entries(stats.byType)) {
        if (count > 0) {
          console.log(`  ${type}: ${count}`);
        }
      }
      console.log('\n最近事件:');
      for (const event of stats.recent.slice(0, 5)) {
        console.log(`  [${event.event_type}] ${event.task || event.learned || '无标题'} (${event.timestamp.split('T')[0]})`);
      }
      
    } else if (command === 'list') {
      const limitIdx = rest.indexOf('--limit');
      const limit = limitIdx !== -1 ? parseInt(rest[limitIdx + 1]) : 10;
      
      const events = await loadEvents(limit);
      console.log(`📋 最近 ${events.length} 个事件:\n`);
      for (const event of events) {
        console.log(`[${event.event_type}] ${event.event_id}`);
        console.log(`  时间：${event.timestamp}`);
        console.log(`  内容：${event.task || event.learned || event.error || '无'}`);
        console.log();
      }
      
    } else {
      console.error(`❌ 未知命令：${command}`);
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ 错误:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

// CLI 入口
const isMainModule = import.meta.url === `file://${process.argv[1]}`;
if (isMainModule) {
  main().catch(console.error);
}
