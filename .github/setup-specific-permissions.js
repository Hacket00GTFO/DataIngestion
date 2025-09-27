#!/usr/bin/env node

/**
 * Script para configurar permisos específicos por branch
 * - Backend: Solo branToRep, HilaryCamacho pueden hacer PR
 * - Frontend: Solo JaobSandoval, solmuz pueden hacer PR
 * - NorbertoSuas: Acceso completo a todo
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
        'User-Agent': 'Specific-Permissions-Setup',
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
          try {
            const parsedData = JSON.parse(responseData);
            reject(new Error(`GitHub API Error: ${res.statusCode} - ${parsedData.message || responseData}`));
          } catch (e) {
            reject(new Error(`GitHub API Error: ${res.statusCode} - ${responseData}`));
          }
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

// Configurar protección para Backend
async function setupBackendProtection() {
  try {
    console.log('🔧 Configurando protección para Backend...');
    
    const protectionRules = {
      required_status_checks: {
        strict: false,
        contexts: []
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 1,
        dismiss_stale_reviews: true,
        require_code_owner_reviews: true,
        bypass_pull_request_allowances: {
          users: ['NorbertoSuas'], // NorbertoSuas puede hacer bypass
          teams: []
        }
      },
      restrictions: {
        users: ['branToRep', 'HilaryCamacho', 'NorbertoSuas'], // Solo estos pueden hacer PR
        teams: [],
        apps: []
      },
      allow_force_pushes: false,
      allow_deletions: false,
      block_creations: false,
      required_conversation_resolution: false
    };
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/Backend/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log('✅ Backend configurado: Solo branToRep, HilaryCamacho, NorbertoSuas pueden hacer PR');
    
  } catch (error) {
    console.error('❌ Error configurando Backend:', error.message);
  }
}

// Configurar protección para Frontend
async function setupFrontendProtection() {
  try {
    console.log('🔧 Configurando protección para Frontend...');
    
    const protectionRules = {
      required_status_checks: {
        strict: false,
        contexts: []
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 1,
        dismiss_stale_reviews: true,
        require_code_owner_reviews: true,
        bypass_pull_request_allowances: {
          users: ['NorbertoSuas'], // NorbertoSuas puede hacer bypass
          teams: []
        }
      },
      restrictions: {
        users: ['JaobSandoval', 'solmuz', 'NorbertoSuas'], // Solo estos pueden hacer PR
        teams: [],
        apps: []
      },
      allow_force_pushes: false,
      allow_deletions: false,
      block_creations: false,
      required_conversation_resolution: false
    };
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/Frontend/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log('✅ Frontend configurado: Solo JaobSandoval, solmuz, NorbertoSuas pueden hacer PR');
    
  } catch (error) {
    console.error('❌ Error configurando Frontend:', error.message);
  }
}

// Configurar protección para Development
async function setupDevelopmentProtection() {
  try {
    console.log('🔧 Configurando protección para Development...');
    
    const protectionRules = {
      required_status_checks: {
        strict: true,
        contexts: ['Sync Child Branches with Development']
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 1,
        dismiss_stale_reviews: true,
        require_code_owner_reviews: true,
        bypass_pull_request_allowances: {
          users: ['NorbertoSuas'], // NorbertoSuas puede hacer bypass
          teams: []
        }
      },
      restrictions: {
        users: ['branToRep', 'HilaryCamacho', 'JaobSandoval', 'solmuz', 'NorbertoSuas'],
        teams: [],
        apps: []
      },
      allow_force_pushes: false,
      allow_deletions: false,
      block_creations: false,
      required_conversation_resolution: false
    };
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/Development/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log('✅ Development configurado: Todos los usuarios autorizados pueden hacer PR');
    
  } catch (error) {
    console.error('❌ Error configurando Development:', error.message);
  }
}

async function main() {
  console.log('🚀 Configurando permisos específicos por branch...\n');
  
  if (!CONFIG.token) {
    console.error('❌ Error: GITHUB_TOKEN no está configurado.');
    console.log('💡 Configúralo con: $env:GITHUB_TOKEN="tu_token_aqui"');
    process.exit(1);
  }
  
  await setupBackendProtection();
  await setupFrontendProtection();
  await setupDevelopmentProtection();
  
  console.log('\n🎉 Configuración completada!');
  console.log('\n📋 Resumen de permisos:');
  console.log('🔧 Backend: Solo branToRep, HilaryCamacho, NorbertoSuas pueden hacer PR');
  console.log('🎨 Frontend: Solo JaobSandoval, solmuz, NorbertoSuas pueden hacer PR');
  console.log('🌿 Development: Todos los usuarios autorizados pueden hacer PR');
  console.log('👑 NorbertoSuas: Acceso completo a todo el repositorio');
}

if (require.main === module) {
  main().catch(console.error);
}
