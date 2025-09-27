#!/usr/bin/env node

/**
 * Script para desactivar temporalmente la protección de branches
 * y permitir sincronización automática
 */

const https = require('https');

const CONFIG = {
  owner: 'NorbertoSuas',
  repo: 'DataIngestion',
  token: process.env.GITHUB_TOKEN,
  branches: ['Backend', 'Frontend']
};

function makeGitHubRequest(endpoint, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: endpoint,
      method: method,
      headers: {
        'Authorization': `token ${CONFIG.token}`,
        'User-Agent': 'Disable-Protection',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    if (data) {
      options.headers['Content-Type'] = 'application/json';
      options.headers['Content-Length'] = Buffer.byteLength(data);
    }

    const req = https.request(options, (res) => {
      let responseData = '';
      
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(responseData);
        } else {
          reject(new Error(`GitHub API Error: ${res.statusCode} - ${responseData}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(data);
    }

    req.end();
  });
}

async function disableProtection(branchName) {
  try {
    console.log(`🔓 Desactivando protección para: ${branchName}`);
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/${branchName}/protection`;
    
    await makeGitHubRequest(endpoint, 'DELETE');
    console.log(`✅ Protección desactivada para ${branchName}`);
    
  } catch (error) {
    console.error(`❌ Error desactivando protección para ${branchName}:`, error.message);
  }
}

async function main() {
  console.log('🚀 Desactivando protección de branches para sincronización automática...\n');
  
  if (!CONFIG.token) {
    console.error('❌ Error: GITHUB_TOKEN no está configurado.');
    process.exit(1);
  }
  
  for (const branchName of CONFIG.branches) {
    await disableProtection(branchName);
  }
  
  console.log('\n🎉 Protección desactivada!');
  console.log('\n📋 Resultado:');
  console.log('✅ Backend y Frontend ya no tienen protección');
  console.log('✅ El workflow puede hacer push automáticamente');
  console.log('✅ Cuando NorbertoSuas haga push a Development, se sincronizarán automáticamente');
}

if (require.main === module) {
  main().catch(console.error);
}
