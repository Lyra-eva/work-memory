#!/usr/bin/env tsx
/**
 * 进化上下文注入器
 * 
 * 用法：
 *   tsx inject-context.ts
 * 
 * 功能：
 *   读取进化模式，生成 prompt 注入文本
 *   在会话开始时调用，让 AI 记住历史经验
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const PATTERNS_FILE = join(process.env.HOME || '~', '.openclaw/workspace/memory/evolution/patterns.json');
const MEMORY_FILE = join(process.env.HOME || '~', '.openclaw/workspace/MEMORY.md');

async function loadPatterns() {
  if (!existsSync(PATTERNS_FILE)) {
    return [];
  }
  return JSON.parse(await readFile(PATTERNS_FILE, 'utf-8'));
}

async function loadMemory() {
  if (!existsSync(MEMORY_FILE)) {
    return '';
  }
  return await readFile(MEMORY_FILE, 'utf-8');
}

async function main() {
  const patterns = await loadPatterns();
  const memory = await loadMemory();
  
  console.log('🧬 进化上下文注入');
  console.log('='.repeat(40));
  
  // 生成 prompt 注入
  const promptInjection = `
## 已学能力与经验

${patterns.length > 0 ? patterns.map((p: any) => `- [${p.type.toUpperCase()}] ${p.name}: ${p.recommendation}`).join('\n') : '暂无积累的模式'}

## 历史教训

${patterns.filter((p: any) => p.type === 'failure').length > 0 
  ? patterns.filter((p: any) => p.type === 'failure').map((p: any) => `⚠️  避免：${p.description} → ${p.recommendation}`).join('\n')
  : '暂无失败记录'}

## 成功模式

${patterns.filter((p: any) => p.type === 'success').length > 0
  ? patterns.filter((p: any) => p.type === 'success').map((p: any) => `✅ 保持：${p.description}`).join('\n')
  : '暂无成功模式'}
`.trim();
  
  console.log('\n📋 Prompt 注入内容:\n');
  console.log(promptInjection);
  console.log('\n' + '='.repeat(40));
  console.log(`💡 将此内容添加到 system prompt 中，让 AI 记住历史经验`);
  
  // 输出为 JSON 格式，方便程序调用
  console.log('\n📦 JSON 格式:');
  console.log(JSON.stringify({
    patterns_count: patterns.length,
    success_patterns: patterns.filter((p: any) => p.type === 'success').length,
    failure_patterns: patterns.filter((p: any) => p.type === 'failure').length,
    injection: promptInjection,
  }, null, 2));
}

main().catch(console.error);
