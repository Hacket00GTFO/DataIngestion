#!/usr/bin/env node

/**
 * Script para configurar la sincronización automática
 * Permite que GitHub Actions haga push automáticamente a Backend y Frontend
 */

const https = require('https');

// Configuración
const CONFIG = {
  owner: 'NorbertoSuas',
  repo: 'DataIngestion',
  token: process.env.GITHUB_TOKEN,
  branches: ['Backend', 'Frontend']
};

// Función para hacer peticiones a la API de GitHub
function makeGitHubRequest(endpoint, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: endpoint,
      method: method,
      headers: {
        'Authorization': `token ${CONFIG.token}`,
        'User-Agent': 'Auto-Sync-Setup',
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
        try {
          const parsedData = JSON.parse(responseData);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(parsedData);
          } else {
            reject(new Error(`GitHub API Error: ${res.statusCode} - ${parsedData.message || responseData}`));
          }
        } catch (e) {
          resolve(responseData);
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

// Configurar protección para sincronización automática
async function configureAutoSync(branchName) {
  try {
    console.log(`🔧 Configurando sincronización automática para: ${branchName}`);
    
    // Configuración específica para sincronización automática
    const protectionRules = {
      required_status_checks: {
        strict: false,
        contexts: []
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 0,
        dismiss_stale_reviews: false,
        require_code_owner_reviews: false,
        bypass_pull_request_allowances: {
          users: ['NorbertoSuas'],
          teams: []
        }
      },
      restrictions: null,
      allow_force_pushes: false,
      allow_deletions: false,
      block_creations: false,
      required_conversation_resolution: false
    };
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/${branchName}/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log(`✅ ${branchName} configurado para sincronización automática`);
    
  } catch (error) {
    console.error(`❌ Error configurando ${branchName}:`, error.message);
  }
}

// Función principal
async function main() {
  console.log('🚀 Configurando sincronización automática...\n');
  
  // Verificar token
  if (!CONFIG.token) {
    console.error('❌ Error: GITHUB_TOKEN no está configurado.');
    console.log('💡 Configúralo con: $env:GITHUB_TOKEN="tu_token_aqui"');
    process.exit(1);
  }
  
  // Configurar cada branch
  for (const branchName of CONFIG.branches) {
    await configureAutoSync(branchName);
  }
  
  console.log('\n🎉 Configuración completada!');
  console.log('\n📋 Resultado:');
  console.log('✅ Cuando NorbertoSuas haga push a Development:');
  console.log('  - Backend se sincronizará automáticamente');
  console.log('  - Frontend se sincronizará automáticamente');
  console.log('✅ Los otros usuarios seguirán necesitando PRs para Backend/Frontend');
}

// Ejecutar
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { configureAutoSync, makeGitHubRequest };
