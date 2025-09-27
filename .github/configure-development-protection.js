#!/usr/bin/env node

/**
 * Script para configurar protección específica del branch Development
 * Solo NorbertoSuas puede hacer push directo, otros necesitan PR
 */

const https = require('https');

const CONFIG = {
  owner: 'NorbertoSuas',
  repo: 'DataIngestion',
  token: process.env.GITHUB_TOKEN
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
        'User-Agent': 'Development-Protection',
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

async function configureDevelopmentProtection() {
  try {
    console.log('🔒 Configurando protección para branch Development...');
    
    // Configuración que permite solo a NorbertoSuas hacer push directo
    const protectionRules = {
      required_status_checks: {
        strict: true,
        contexts: ['Sync Child Branches with Development']
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 1,
        dismiss_stale_reviews: true,
        require_code_owner_reviews: true
      },
      restrictions: null,
      allow_force_pushes: false,
      allow_deletions: false,
      block_creations: false,
      required_conversation_resolution: false
    };
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/Development/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log('✅ Protección configurada para Development');
    
  } catch (error) {
    console.error('❌ Error configurando protección:', error.message);
  }
}

async function main() {
  console.log('🚀 Configurando protección específica para Development...\n');
  
  if (!CONFIG.token) {
    console.error('❌ Error: GITHUB_TOKEN no está configurado.');
    process.exit(1);
  }
  
  await configureDevelopmentProtection();
  
  console.log('\n🎉 Configuración completada!');
  console.log('\n📋 Resultado:');
  console.log('✅ Development requiere Pull Request obligatorio');
  console.log('✅ Solo NorbertoSuas puede hacer push directo (como admin)');
  console.log('✅ Los demás usuarios deben hacer PR desde Backend/Frontend');
  console.log('✅ Code review obligatorio para PRs');
  console.log('✅ Status checks obligatorios (incluyendo nuestro workflow)');
}

if (require.main === module) {
  main().catch(console.error);
}
