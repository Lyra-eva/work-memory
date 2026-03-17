#!/usr/bin/env tsx
/**
 * 进化事件收集器
 * 
 * 用法：
 *   tsx collect-event.ts <event_type> <data_json>
 * 
 * 示例：
 *   tsx collect-event.ts success '{"task":"回答用户问题","duration_ms":1200}'
 *   tsx collect-event.ts failure '{"task":"浏览器自动化","error":"timeout"}'
 *   tsx collect-event.ts lesson '{"what":"用户纠正了我","learned":"需要确认时区"}'
 */

import { appendFile, readFile, writeFile } from 'fs/promises';
import { join } from 'path';

const EVOLUTION_DIR = join(process.env.HOME || '~', '.openclaw/workspace/memory/evolution');
const EVENTS_FILE = join(EVOLUTION_DIR, 'events.jsonl');
const INDEX_FILE = join(EVOLUTION_DIR, 'index.json');

interface EvolutionEvent {
  event_id: string;
  event_type: 'success' | 'failure' | 'lesson' | 'pattern' | 'capability';
  timestamp: string;
  session_id?: string;
  task?: string;
  input?: string;
  output?: string;
  feedback?: string;
  error?: string;
  learned?: string;
  confidence?: number;
  importance?: number;
  tags?: string[];
  meta?: Record<string, any>;
}

async function ensureDir() {
  const { mkdir } = await import('fs/promises');
  await mkdir(EVOLUTION_DIR, { recursive: true });
}

async function appendEvent(event: EvolutionEvent) {
  const line = JSON.stringify(event) + '\n';
  await appendFile(EVENTS_FILE, line, 'utf-8');
  console.log(`✅ 事件已记录：${event.event_type} [${event.event_id}]`);
}

async function updateIndex(event: EvolutionEvent) {
  let index = { total_events: 0, events: [] as any[] };
  try {
    const content = await readFile(INDEX_FILE, 'utf-8');
    index = JSON.parse(content);
  } catch {
    // 文件不存在，使用默认值
  }
  
  index.total_events++;
  index.events.push({
    event_id: event.event_id,
    event_type: event.event_type,
    timestamp: event.timestamp,
  });
  
  // 只保留最近 100 条索引
  if (index.events.length > 100) {
    index.events = index.events.slice(-100);
  }
  
  await writeFile(INDEX_FILE, JSON.stringify(index, null, 2), 'utf-8');
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
🧬 进化事件收集器

用法：
  tsx collect-event.ts <event_type> <data_json>

事件类型：
  success   - 成功事件
  failure   - 失败事件
  lesson    - 经验教训
  pattern   - 发现模式
  capability - 新能力

示例：
  tsx collect-event.ts success '{"task":"回答问题","duration_ms":1200}'
  tsx collect-event.ts failure '{"task":"浏览器","error":"timeout"}'
  tsx collect-event.ts lesson '{"what":"用户纠正","learned":"确认时区"}'
`);
    process.exit(1);
  }
  
  const [eventType, dataJson] = args;
  
  const validTypes = ['success', 'failure', 'lesson', 'pattern', 'capability'];
  if (!validTypes.includes(eventType)) {
    console.error(`❌ 无效的事件类型：${eventType}`);
    console.error(`有效类型：${validTypes.join(', ')}`);
    process.exit(1);
  }
  
  let data: Record<string, any>;
  try {
    data = JSON.parse(dataJson);
  } catch (e) {
    console.error(`❌ JSON 解析失败：${dataJson}`);
    process.exit(1);
  }
  
  await ensureDir();
  
  const event: EvolutionEvent = {
    event_id: `evt_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    event_type: eventType as EvolutionEvent['event_type'],
    timestamp: new Date().toISOString(),
    ...data,
    importance: data.importance || 0.5,
    tags: data.tags || [],
  };
  
  await appendEvent(event);
  await updateIndex(event);
  
  console.log(`📊 当前总事件数：${(await readFile(INDEX_FILE, 'utf-8').then(JSON.parse)).total_events}`);
}

main().catch(console.error);
