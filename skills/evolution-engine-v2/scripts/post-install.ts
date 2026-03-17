#!/usr/bin/env tsx
/**
 * 安装后初始化脚本
 * 
 * 自动创建数据目录和配置文件
 */

import { mkdir, writeFile } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const HOME = process.env.HOME || '~';
const DATA_DIR = join(HOME, '.openclaw/workspace/memory/evolution');
const CONFIG_FILE = join(HOME, '.openclaw/workspace/evolution-config.json');

async function main() {
  console.log('🧬 Evolution Engine v2 - 安装后初始化\n');
  
  // 创建数据目录
  console.log('📁 创建数据目录...');
  await mkdir(DATA_DIR, { recursive: true });
  console.log(`✅ 数据目录：${DATA_DIR}\n`);
  
  // 创建默认配置
  console.log('⚙️  创建默认配置...');
  const defaultConfig = {
    enabled: true,
    autoCollect: true,
    autoReflect: 'daily',
    reflectTime: '0 3 * * *',
    maxEvents: 10000,
    injectContext: true,
  };
  
  if (!existsSync(CONFIG_FILE)) {
    await writeFile(CONFIG_FILE, JSON.stringify(defaultConfig, null, 2), 'utf-8');
    console.log(`✅ 配置文件：${CONFIG_FILE}\n`);
  } else {
    console.log('ℹ️  配置文件已存在，跳过\n');
  }
  
  console.log('✅ 安装完成！\n');
  console.log('📚 下一步:');
  console.log('  1. 启用自动进化:');
  console.log('     npx tsx src/openclaw-integration.ts enable\n');
  console.log('  2. 记录第一个事件:');
  console.log('     npx tsx src/event-collector.ts collect --type success --data \'{"task":"安装成功"}\'\n');
  console.log('  3. 查看文档:');
  console.log('     cat SKILL.md\n');
}

main().catch(console.error);
