#!/usr/bin/env tsx
/**
 * 进化反思引擎
 * 
 * 用法：
 *   tsx reflect.ts [--dry-run]
 * 
 * 功能：
 *   1. 读取所有进化事件
 *   2. 分析成功/失败模式
 *   3. 提取经验教训
 *   4. 生成能力更新建议
 *   5. 输出到 MEMORY.md
 */

import { readFile, writeFile, appendFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const EVOLUTION_DIR = join(process.env.HOME || '~', '.openclaw/workspace/memory/evolution');
const EVENTS_FILE = join(EVOLUTION_DIR, 'events.jsonl');
const PATTERNS_FILE = join(EVOLUTION_DIR, 'patterns.json');
const MEMORY_FILE = join(process.env.HOME || '~', '.openclaw/workspace/MEMORY.md');

interface EvolutionEvent {
  event_id: string;
  event_type: string;
  timestamp: string;
  task?: string;
  input?: string;
  output?: string;
  error?: string;
  learned?: string;
  importance?: number;
  tags?: string[];
}

interface Pattern {
  pattern_id: string;
  type: 'success' | 'failure' | 'bottleneck' | 'opportunity';
  name: string;
  description: string;
  occurrences: number;
  confidence: number;
  recommendation: string;
  discovered_at: string;
}

async function loadEvents(): Promise<EvolutionEvent[]> {
  if (!existsSync(EVENTS_FILE)) {
    console.log('⚠️  事件文件不存在，跳过');
    return [];
  }
  
  const content = await readFile(EVENTS_FILE, 'utf-8');
  const events: EvolutionEvent[] = [];
  
  for (const line of content.split('\n')) {
    if (line.trim()) {
      try {
        events.push(JSON.parse(line));
      } catch {
        // 跳过无效行
      }
    }
  }
  
  return events;
}

function analyzePatterns(events: EvolutionEvent[]): Pattern[] {
  const patterns: Pattern[] = [];
  
  // 按类型分组
  const byType = new Map<string, EvolutionEvent[]>();
  for (const event of events) {
    const key = event.event_type;
    if (!byType.has(key)) byType.set(key, []);
    byType.get(key)!.push(event);
  }
  
  // 分析成功模式
  const successes = byType.get('success') || [];
  if (successes.length >= 2) {
    const taskCounts = new Map<string, number>();
    for (const s of successes) {
      const task = s.task || 'unknown';
      taskCounts.set(task, (taskCounts.get(task) || 0) + 1);
    }
    
    for (const [task, count] of taskCounts) {
      if (count >= 2) {
        patterns.push({
          pattern_id: `success_${task.replace(/\s+/g, '_')}`,
          type: 'success',
          name: `成功模式：${task}`,
          description: `在"${task}"任务上成功了${count}次`,
          occurrences: count,
          confidence: Math.min(0.5 + count * 0.15, 0.95),
          recommendation: `继续优化"${task}"的处理方式`,
          discovered_at: new Date().toISOString(),
        });
      }
    }
  }
  
  // 分析失败模式
  const failures = byType.get('failure') || [];
  if (failures.length >= 1) {
    const errorCounts = new Map<string, number>();
    for (const f of failures) {
      const error = f.error || 'unknown';
      errorCounts.set(error, (errorCounts.get(error) || 0) + 1);
    }
    
    for (const [error, count] of errorCounts) {
      patterns.push({
        pattern_id: `failure_${error.replace(/\s+/g, '_')}`,
        type: 'failure',
        name: `失败模式：${error}`,
        description: `因"${error}"失败了${count}次`,
        occurrences: count,
        confidence: Math.min(0.6 + count * 0.2, 0.95),
        recommendation: `需要解决"${error}"问题`,
        discovered_at: new Date().toISOString(),
      });
    }
  }
  
  // 分析经验教训
  const lessons = byType.get('lesson') || [];
  if (lessons.length >= 1) {
    patterns.push({
      pattern_id: `lessons_${lessons.length}`,
      type: 'opportunity',
      name: `经验教训`,
      description: `积累了${lessons.length}条经验教训`,
      occurrences: lessons.length,
      confidence: 0.8,
      recommendation: lessons.map(l => l.learned).filter(Boolean).join('; ') || '继续积累',
      discovered_at: new Date().toISOString(),
    });
  }
  
  return patterns;
}

async function updateMemory(patterns: Pattern[], dryRun = false) {
  const timestamp = new Date().toISOString().split('T')[0];
  
  const evolutionSection = `
## 🧬 进化引擎 (自动更新)

**最后更新**: ${timestamp}

### 发现的模式

${patterns.map(p => `- **${p.name}** (置信度：${(p.confidence * 100).toFixed(0)}%)
  - ${p.description}
  - 建议：${p.recommendation}`).join('\n\n')}

### 能力成长

${patterns.filter(p => p.type === 'success').length} 个成功模式，${patterns.filter(p => p.type === 'failure').length} 个待改进点

---
`;
  
  if (dryRun) {
    console.log('\n📝 将更新 MEMORY.md:\n');
    console.log(evolutionSection);
    return;
  }
  
  let memoryContent = '';
  if (existsSync(MEMORY_FILE)) {
    memoryContent = await readFile(MEMORY_FILE, 'utf-8');
    
    // 删除旧的进化引擎部分
    const startIdx = memoryContent.indexOf('## 🧬 进化引擎');
    if (startIdx !== -1) {
      const endIdx = memoryContent.indexOf('---', startIdx + 10);
      if (endIdx !== -1) {
        memoryContent = memoryContent.slice(0, startIdx) + memoryContent.slice(endIdx + 4);
      }
    }
  }
  
  // 追加新部分
  memoryContent = memoryContent.trimEnd() + '\n\n' + evolutionSection;
  
  await writeFile(MEMORY_FILE, memoryContent, 'utf-8');
  console.log('✅ MEMORY.md 已更新');
}

async function savePatterns(patterns: Pattern[]) {
  let existing: Pattern[] = [];
  if (existsSync(PATTERNS_FILE)) {
    existing = JSON.parse(await readFile(PATTERNS_FILE, 'utf-8'));
  }
  
  // 合并新模式（去重）
  const existingIds = new Set(existing.map(p => p.pattern_id));
  for (const p of patterns) {
    if (!existingIds.has(p.pattern_id)) {
      existing.push(p);
    }
  }
  
  // 只保留最近 50 个模式
  if (existing.length > 50) {
    existing = existing.slice(-50);
  }
  
  await writeFile(PATTERNS_FILE, JSON.stringify(existing, null, 2), 'utf-8');
  console.log(`✅ 已保存 ${patterns.length} 个模式`);
}

async function main() {
  const dryRun = process.argv.includes('--dry-run');
  
  console.log('🧬 进化反思引擎');
  console.log('=' .repeat(40));
  
  const events = await loadEvents();
  console.log(`📊 加载了 ${events.length} 个事件`);
  
  if (events.length === 0) {
    console.log('⚠️  没有事件可分析，先收集一些事件吧');
    console.log('\n💡 用法示例:');
    console.log('  tsx collect-event.ts success \'{"task":"回答问题"}\'');
    return;
  }
  
  const patterns = analyzePatterns(events);
  console.log(`🔍 发现了 ${patterns.length} 个模式`);
  
  await savePatterns(patterns);
  await updateMemory(patterns, dryRun);
  
  console.log('\n' + '='.repeat(40));
  console.log('✅ 反思完成');
  
  if (dryRun) {
    console.log('\n⚠️  这是预演模式，实际运行请去掉 --dry-run');
  }
}

main().catch(console.error);
