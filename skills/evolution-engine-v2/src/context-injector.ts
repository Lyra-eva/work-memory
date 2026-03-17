#!/usr/bin/env tsx
/**
 * 进化上下文注入器 v2
 * 
 * 在会话开始时读取历史模式，生成 prompt 注入
 * 
 * 用法:
 *   tsx context-injector.ts [--json]
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { Pattern } from './reflector.js';

// ============================================================
// 配置
// ============================================================

const WORKSPACE_DIR = join(process.env.HOME || '~', '.openclaw/workspace');
const PATTERNS_FILE = join(WORKSPACE_DIR, 'memory/evolution/patterns.json');
const MEMORY_FILE = join(WORKSPACE_DIR, 'MEMORY.md');

// ============================================================
// 加载模式
// ============================================================

async function loadPatterns(): Promise<Pattern[]> {
  if (!existsSync(PATTERNS_FILE)) {
    return [];
  }
  return JSON.parse(await readFile(PATTERNS_FILE, 'utf-8'));
}

// ============================================================
// 生成 Prompt 注入
// ============================================================

export function generateInjection(patterns: Pattern[]): string {
  if (patterns.length === 0) {
    return '## 进化状态\n\n暂无历史经验积累，从第一次交互开始学习。';
  }
  
  const successPatterns = patterns.filter(p => p.type === 'success');
  const failurePatterns = patterns.filter(p => p.type === 'failure' || p.type === 'bottleneck');
  const opportunityPatterns = patterns.filter(p => p.type === 'opportunity');
  const habitPatterns = patterns.filter(p => p.type === 'habit');
  
  const sections: string[] = [];
  
  // 成功模式
  if (successPatterns.length > 0) {
    sections.push(`## ✅ 已验证的成功方法

${successPatterns.map(p => `- **${p.name}**: ${p.recommendation}`).join('\n')}`);
  }
  
  // 失败教训
  if (failurePatterns.length > 0) {
    sections.push(`## ⚠️ 需要避免的错误

${failurePatterns.map(p => `- **${p.name}**: ${p.recommendation}`).join('\n')}

**重要**: 以上错误已发生过${failurePatterns.reduce((sum, p) => sum + p.occurrences, 0)}次，务必避免重蹈覆辙。`);
  }
  
  // 经验教训
  if (opportunityPatterns.length > 0) {
    sections.push(`## 📚 积累的经验

${opportunityPatterns.map(p => `- ${p.name}: ${p.recommendation}`).join('\n')}`);
  }
  
  // 用户习惯
  if (habitPatterns.length > 0) {
    sections.push(`## 👤 用户习惯

${habitPatterns.map(p => `- ${p.name}: ${p.description}`).join('\n')}

根据以上习惯，在合适的时间主动提供相关服务。`);
  }
  
  // 生成总结
  const summary = `
## 🎯 当前进化状态

- **成功模式**: ${successPatterns.length} 个
- **待改进**: ${failurePatterns.length} 个
- **经验教训**: ${opportunityPatterns.length} 个
- **用户习惯**: ${habitPatterns.length} 个

**行动优先级**:
${failurePatterns.slice(0, 3).map((p, i) => `${i + 1}. 优先解决：${p.name}`).join('\n') || '暂无紧急改进项'}
`;
  
  sections.unshift(summary);
  
  return sections.join('\n\n');
}

// ============================================================
// 加载完整上下文（包括 MEMORY.md）
// ============================================================

export async function loadFullContext(): Promise<string> {
  const patterns = await loadPatterns();
  const injection = generateInjection(patterns);
  
  let memoryContent = '';
  if (existsSync(MEMORY_FILE)) {
    memoryContent = await readFile(MEMORY_FILE, 'utf-8');
    
    // 提取 MEMORY.md 中的关键部分
    const relevantSections: string[] = [];
    
    // 提取 Preferences
    const prefMatch = memoryContent.match(/## Preferences\n([\s\S]*?)(?=##|$)/);
    if (prefMatch) {
      relevantSections.push(`## 用户偏好\n${prefMatch[1]}`);
    }
    
    // 提取 Notes
    const notesMatch = memoryContent.match(/## Notes\n([\s\S]*?)(?=##|$)/);
    if (notesMatch) {
      relevantSections.push(`## 重要备注\n${notesMatch[1]}`);
    }
    
    // 提取进化引擎部分
    const evolutionMatch = memoryContent.match(/## 🧬 进化引擎[\s\S]*?(?=##|$)/);
    if (evolutionMatch) {
      // 已经通过 patterns 生成了，这里不需要重复
    }
    
    if (relevantSections.length > 0) {
      return `# 会话上下文\n\n${injection}\n\n${relevantSections.join('\n\n')}`;
    }
  }
  
  return `# 会话上下文\n\n${injection}`;
}

// ============================================================
// CLI 入口
// ============================================================

async function main(): Promise<void> {
  const asJson = process.argv.includes('--json');
  
  const patterns = await loadPatterns();
  const injection = generateInjection(patterns);
  
  if (asJson) {
    const output = {
      patterns_count: patterns.length,
      success_patterns: patterns.filter(p => p.type === 'success').length,
      failure_patterns: patterns.filter(p => p.type === 'failure' || p.type === 'bottleneck').length,
      opportunity_patterns: patterns.filter(p => p.type === 'opportunity').length,
      habit_patterns: patterns.filter(p => p.type === 'habit').length,
      injection: injection,
      full_context: await loadFullContext(),
    };
    console.log(JSON.stringify(output, null, 2));
  } else {
    console.log('🧬 进化上下文注入 v2');
    console.log('='.repeat(40));
    console.log('\n📋 Prompt 注入内容:\n');
    console.log(injection);
    console.log('\n' + '='.repeat(40));
    console.log(`💡 将此内容添加到 system prompt 中`);
    console.log(`📊 当前有 ${patterns.length} 个历史模式可复用`);
  }
}

// CLI 入口
const isMainModule = import.meta.url === `file://${process.argv[1]}`;
if (isMainModule) {
  main().catch(console.error);
}
