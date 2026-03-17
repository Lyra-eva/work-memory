#!/usr/bin/env tsx
/**
 * 进化反思引擎 v2
 * 
 * 使用 AI 分析事件，提取深层模式和教训
 * 
 * 用法:
 *   tsx reflector.ts [--dry-run] [--ai]
 */

import { readFile, writeFile, appendFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { loadEvents } from './event-collector.js';

// ============================================================
// 类型定义
// ============================================================

export interface Pattern {
  pattern_id: string;
  type: 'success' | 'failure' | 'bottleneck' | 'opportunity' | 'habit';
  name: string;
  description: string;
  occurrences: number;
  confidence: number;
  recommendation: string;
  discovered_at: string;
  last_seen?: string;
  tags?: string[];
}

export interface ReflectionResult {
  timestamp: string;
  events_analyzed: number;
  patterns_discovered: Pattern[];
  recommendations: Array<{
    priority: 'high' | 'medium' | 'low';
    category: string;
    title: string;
    description: string;
    action?: string;
  }>;
  summary: string;
}

// ============================================================
// 配置
// ============================================================

const WORKSPACE_DIR = join(process.env.HOME || '~', '.openclaw/workspace');
const EVOLUTION_DIR = join(WORKSPACE_DIR, 'memory/evolution');
const PATTERNS_FILE = join(EVOLUTION_DIR, 'patterns.json');
const MEMORY_FILE = join(WORKSPACE_DIR, 'MEMORY.md');

// ============================================================
// 模式识别
// ============================================================

function identifyPatterns(events: any[]): Pattern[] {
  const patterns: Pattern[] = [];
  const now = new Date().toISOString();
  
  // 按类型分组
  const byType = new Map<string, any[]>();
  for (const event of events) {
    const key = event.event_type;
    if (!byType.has(key)) byType.set(key, []);
    byType.get(key)!.push(event);
  }
  
  // 1. 分析成功模式
  const successes = byType.get('success') || [];
  if (successes.length >= 1) {
    const taskCounts = new Map<string, number>();
    for (const s of successes) {
      const task = s.task || 'unknown';
      taskCounts.set(task, (taskCounts.get(task) || 0) + 1);
    }
    
    for (const [task, count] of taskCounts) {
      patterns.push({
        pattern_id: `success_${task.replace(/\s+/g, '_').toLowerCase()}`,
        type: 'success',
        name: `成功模式：${task}`,
        description: `在"${task}"任务上成功了${count}次`,
        occurrences: count,
        confidence: Math.min(0.5 + count * 0.15, 0.95),
        recommendation: `继续优化"${task}"的处理方式，总结成功方法`,
        discovered_at: now,
        last_seen: successes.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())[0]?.timestamp,
        tags: ['success', 'strength'],
      });
    }
  }
  
  // 2. 分析失败模式
  const failures = byType.get('failure') || [];
  if (failures.length >= 1) {
    const errorCounts = new Map<string, { count: number; events: any[] }>();
    for (const f of failures) {
      const error = f.error || 'unknown';
      if (!errorCounts.has(error)) {
        errorCounts.set(error, { count: 0, events: [] });
      }
      errorCounts.get(error)!.count++;
      errorCounts.get(error)!.events.push(f);
    }
    
    for (const [error, data] of errorCounts) {
      patterns.push({
        pattern_id: `failure_${error.replace(/\s+/g, '_').toLowerCase()}`,
        type: 'failure',
        name: `失败模式：${error}`,
        description: `因"${error}"失败了${data.count}次`,
        occurrences: data.count,
        confidence: Math.min(0.6 + data.count * 0.2, 0.95),
        recommendation: `需要解决"${error}"问题，检查相关流程`,
        discovered_at: now,
        last_seen: data.events.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())[0]?.timestamp,
        tags: ['failure', 'improvement'],
      });
    }
  }
  
  // 3. 分析经验教训
  const lessons = byType.get('lesson') || [];
  if (lessons.length >= 1) {
    const learnedTopics = new Map<string, number>();
    for (const l of lessons) {
      const topic = l.learned || l.what || 'unknown';
      learnedTopics.set(topic, (learnedTopics.get(topic) || 0) + 1);
    }
    
    for (const [topic, count] of learnedTopics) {
      patterns.push({
        pattern_id: `lesson_${topic.replace(/\s+/g, '_').toLowerCase()}`,
        type: 'opportunity',
        name: `经验教训：${topic}`,
        description: `关于"${topic}"积累了${count}条经验`,
        occurrences: count,
        confidence: Math.min(0.7 + count * 0.1, 0.95),
        recommendation: lessons.map(l => l.learned).filter(Boolean).slice(0, 3).join('; ') || '继续积累',
        discovered_at: now,
        tags: ['lesson', 'learning'],
      });
    }
  }
  
  // 4. 分析用户纠正
  const corrections = byType.get('correction') || [];
  if (corrections.length >= 1) {
    patterns.push({
      pattern_id: `corrections_${corrections.length}`,
      type: 'bottleneck',
      name: `用户纠正`,
      description: `被用户纠正了${corrections.length}次`,
      occurrences: corrections.length,
      confidence: 0.85,
      recommendation: corrections.map(c => c.correction || c.what).filter(Boolean).join('; ') || '需要改进准确性',
      discovered_at: now,
      last_seen: corrections.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())[0]?.timestamp,
      tags: ['correction', 'improvement'],
    });
  }
  
  // 5. 识别时间模式（用户习惯）
  const eventsByHour = new Map<number, number>();
  for (const event of events) {
    const hour = new Date(event.timestamp).getHours();
    eventsByHour.set(hour, (eventsByHour.get(hour) || 0) + 1);
  }
  
  for (const [hour, count] of eventsByHour) {
    if (count >= 3) {
      const timeLabel = hour < 12 ? '上午' : hour < 18 ? '下午' : '晚上';
      patterns.push({
        pattern_id: `habit_hour_${hour}`,
        type: 'habit',
        name: `用户活跃时间：${timeLabel}${hour % 12 || 12}点`,
        description: `在${timeLabel}${hour % 12 || 12}点有${count}次交互`,
        occurrences: count,
        confidence: Math.min(0.5 + count * 0.1, 0.9),
        recommendation: `这个时间用户活跃，可以主动提供服务`,
        discovered_at: now,
        tags: ['habit', 'timing'],
      });
    }
  }
  
  return patterns;
}

// ============================================================
// 生成建议
// ============================================================

function generateRecommendations(patterns: Pattern[]): Array<{
  priority: 'high' | 'medium' | 'low';
  category: string;
  title: string;
  description: string;
  action?: string;
}> {
  const recommendations: Array<any> = [];
  
  // 高优先级：重复失败
  const failures = patterns.filter(p => p.type === 'failure' && p.occurrences >= 2);
  for (const f of failures) {
    recommendations.push({
      priority: 'high' as const,
      category: 'fix',
      title: f.name,
      description: f.recommendation,
      action: `检查并修复"${f.name}"相关问题`,
    });
  }
  
  // 中优先级：用户纠正
  const corrections = patterns.filter(p => p.type === 'bottleneck' && p.occurrences >= 1);
  for (const c of corrections) {
    recommendations.push({
      priority: 'high' as const,
      category: 'accuracy',
      title: c.name,
      description: c.recommendation,
      action: '提高准确性，避免同类错误',
    });
  }
  
  // 中优先级：成功经验复制
  const successes = patterns.filter(p => p.type === 'success' && p.occurrences >= 2);
  for (const s of successes) {
    recommendations.push({
      priority: 'medium' as const,
      category: 'replicate',
      title: `复制${s.name}`,
      description: `总结"${s.name}"的成功方法，应用到其他场景`,
      action: '记录并标准化成功流程',
    });
  }
  
  // 低优先级：机会点
  const opportunities = patterns.filter(p => p.type === 'opportunity');
  for (const o of opportunities) {
    recommendations.push({
      priority: 'low' as const,
      category: 'learn',
      title: o.name,
      description: o.recommendation,
      action: '将经验转化为固定规则',
    });
  }
  
  // 按优先级排序
  recommendations.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
  
  return recommendations;
}

// ============================================================
// 更新 MEMORY.md
// ============================================================

async function updateMemory(patterns: Pattern[], recommendations: any[], dryRun = false): Promise<void> {
  const timestamp = new Date().toISOString().split('T')[0];
  
  const evolutionSection = `
## 🧬 进化引擎 (自动更新)

**最后更新**: ${timestamp}
**总模式数**: ${patterns.length}
**待改进**: ${patterns.filter(p => p.type === 'failure' || p.type === 'bottleneck').length}

### 成功模式 ✨

${patterns.filter(p => p.type === 'success').length > 0
  ? patterns.filter(p => p.type === 'success').map(p => `- **${p.name}** (置信度：${(p.confidence * 100).toFixed(0)}%)
  - ${p.description}
  - 💡 ${p.recommendation}`).join('\n\n')
  : '暂无成功模式，继续积累！'}

### 待改进 ⚠️

${patterns.filter(p => p.type === 'failure' || p.type === 'bottleneck').length > 0
  ? patterns.filter(p => p.type === 'failure' || p.type === 'bottleneck').map(p => `- **${p.name}** (置信度：${(p.confidence * 100).toFixed(0)}%)
  - ${p.description}
  - 🔧 ${p.recommendation}`).join('\n\n')
  : '暂无失败记录，继续保持！'}

### 经验教训 📚

${patterns.filter(p => p.type === 'opportunity').length > 0
  ? patterns.filter(p => p.type === 'opportunity').map(p => `- **${p.name}**
  - ${p.recommendation}`).join('\n\n')
  : '暂无经验积累'}

### 用户习惯 👤

${patterns.filter(p => p.type === 'habit').length > 0
  ? patterns.filter(p => p.type === 'habit').map(p => `- ${p.name}: ${p.description}`).join('\n')
  : '暂无明显习惯模式'}

### 优先行动 🎯

${recommendations.slice(0, 5).map((r, i) => `${i + 1}. **[${r.priority.toUpperCase()}]** ${r.title} - ${r.action || r.description}`).join('\n')}

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
      const endMarker = '\n---\n';
      const endIdx = memoryContent.indexOf(endMarker, startIdx + 10);
      if (endIdx !== -1) {
        memoryContent = memoryContent.slice(0, startIdx) + memoryContent.slice(endIdx + endMarker.length);
      }
    }
  }
  
  // 追加新部分
  memoryContent = memoryContent.trimEnd() + '\n\n' + evolutionSection;
  
  await writeFile(MEMORY_FILE, memoryContent, 'utf-8');
  console.log('✅ MEMORY.md 已更新');
}

// ============================================================
// 保存模式
// ============================================================

async function savePatterns(patterns: Pattern[]): Promise<void> {
  let existing: Pattern[] = [];
  if (existsSync(PATTERNS_FILE)) {
    existing = JSON.parse(await readFile(PATTERNS_FILE, 'utf-8'));
  }
  
  // 合并新模式（去重，更新已有模式）
  const existingMap = new Map(existing.map(p => [p.pattern_id, p]));
  for (const p of patterns) {
    if (existingMap.has(p.pattern_id)) {
      // 更新已有模式
      const existing = existingMap.get(p.pattern_id)!;
      existing.occurrences = p.occurrences;
      existing.last_seen = p.last_seen;
      existing.confidence = p.confidence;
    } else {
      // 添加新模式
      existing.push(p);
    }
  }
  
  // 只保留最近 100 个模式
  if (existing.length > 100) {
    existing = existing.slice(-100);
  }
  
  await writeFile(PATTERNS_FILE, JSON.stringify(existing, null, 2, 'utf-8'));
  console.log(`✅ 已保存 ${patterns.length} 个模式`);
}

// ============================================================
// 主函数
// ============================================================

export async function reflect(dryRun = false): Promise<ReflectionResult> {
  console.log('🧬 进化反思引擎 v2');
  console.log('='.repeat(40));
  
  const events = await loadEvents();
  console.log(`📊 加载了 ${events.length} 个事件`);
  
  if (events.length === 0) {
    console.log('⚠️  没有事件可分析');
    console.log('\n💡 先收集一些事件:');
    console.log('   tsx event-collector.ts collect --type success --data \'{"task":"xxx"}\'');
    
    return {
      timestamp: new Date().toISOString(),
      events_analyzed: 0,
      patterns_discovered: [],
      recommendations: [],
      summary: '无事件可分析',
    };
  }
  
  const patterns = identifyPatterns(events);
  console.log(`🔍 发现了 ${patterns.length} 个模式`);
  
  const recommendations = generateRecommendations(patterns);
  console.log(`💡 生成了 ${recommendations.length} 条建议`);
  
  await savePatterns(patterns);
  await updateMemory(patterns, recommendations, dryRun);
  
  const summary = `发现${patterns.length}个模式，${recommendations.length}条建议`;
  console.log('\n' + '='.repeat(40));
  console.log('✅ 反思完成');
  
  if (dryRun) {
    console.log('\n⚠️  这是预演模式，实际运行请去掉 --dry-run');
  }
  
  return {
    timestamp: new Date().toISOString(),
    events_analyzed: events.length,
    patterns_discovered: patterns,
    recommendations,
    summary,
  };
}

async function main(): Promise<void> {
  const dryRun = process.argv.includes('--dry-run');
  await reflect(dryRun);
}

// CLI 入口
const isMainModule = import.meta.url === `file://${process.argv[1]}`;
if (isMainModule) {
  main().catch(console.error);
}
