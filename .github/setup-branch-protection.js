#!/usr/bin/env node

/**
 * Script para configurar automáticamente las reglas de protección de branches
 * en GitHub usando la API de GitHub
 * 
 * Uso:
 * 1. Configura tu GITHUB_TOKEN como variable de entorno
 * 2. Ejecuta: node .github/setup-branch-protection.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuración
const CONFIG = {
  // Reemplaza con tu información
  owner: 'NorbertoSuas',        // Tu usuario de GitHub (cambiar por el real)
  repo: 'DataIngestion',             // Nombre de tu repositorio
  token: process.env.GITHUB_TOKEN,   // Token de GitHub (configúralo como variable de entorno)
  
  // Branches a proteger
  branches: ['Development', 'Backend', 'Frontend'],
  
  // Configuración de protección
  protection_rules: {
    Development: {
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
      restrictions: null
    },
    Backend: {
      required_status_checks: {
        strict: false,
        contexts: []
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 0,
        dismiss_stale_reviews: false,
        require_code_owner_reviews: false
      },
      restrictions: null,
      allow_force_pushes: false,
      allow_deletions: false
    },
    Frontend: {
      required_status_checks: {
        strict: false,
        contexts: []
      },
      enforce_admins: false,
      required_pull_request_reviews: {
        required_approving_review_count: 0,
        dismiss_stale_reviews: false,
        require_code_owner_reviews: false
      },
      restrictions: null,
      allow_force_pushes: false,
      allow_deletions: false
    }
  }
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
        'User-Agent': 'Branch-Protection-Setup',
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

// Función para configurar protección de un branch
async function setupBranchProtection(branchName, protectionRules) {
  try {
    console.log(`🔒 Configurando protección para branch: ${branchName}`);
    
    const endpoint = `/repos/${CONFIG.owner}/${CONFIG.repo}/branches/${branchName}/protection`;
    const data = JSON.stringify(protectionRules);
    
    await makeGitHubRequest(endpoint, 'PUT', data);
    console.log(`✅ Protección configurada exitosamente para ${branchName}`);
    
  } catch (error) {
    if (error.message.includes('404')) {
      console.log(`⚠️  Branch ${branchName} no existe. Se creará cuando se haga el primer push.`);
    } else {
      console.error(`❌ Error configurando protección para ${branchName}:`, error.message);
    }
  }
}

// Función principal
async function main() {
  console.log('🚀 Iniciando configuración de protección de branches...\n');
  
  // Verificar que el token esté configurado
  if (!CONFIG.token) {
    console.error('❌ Error: GITHUB_TOKEN no está configurado.');
    console.log('💡 Configúralo con: export GITHUB_TOKEN=tu_token_aqui');
    process.exit(1);
  }
  
  // Verificar conectividad con GitHub
  try {
    console.log('🔍 Verificando conectividad con GitHub...');
    console.log(`📍 Endpoint: /repos/${CONFIG.owner}/${CONFIG.repo}`);
    console.log(`🔑 Token configurado: ${CONFIG.token ? 'Sí' : 'No'}`);
    await makeGitHubRequest(`/repos/${CONFIG.owner}/${CONFIG.repo}`);
    console.log('✅ Conexión exitosa con GitHub\n');
  } catch (error) {
    console.error('❌ Error conectando con GitHub:', error.message);
    console.log('💡 Verifica tu GITHUB_TOKEN y los nombres de owner/repo');
    process.exit(1);
  }
  
  // Configurar protección para cada branch
  for (const branchName of CONFIG.branches) {
    const protectionRules = CONFIG.protection_rules[branchName];
    if (protectionRules) {
      await setupBranchProtection(branchName, protectionRules);
    } else {
      console.log(`⚠️  No se encontraron reglas de protección para ${branchName}`);
    }
  }
  
  console.log('\n🎉 Configuración de protección completada!');
  console.log('\n📋 Próximos pasos:');
  console.log('1. Edita .github/branch-protection.yml con tus usuarios reales');
  console.log('2. Crea equipos en GitHub si planeas usarlos');
  console.log('3. Configura CODEOWNERS si necesitas code review obligatorio');
  console.log('4. Prueba haciendo un push a cada branch para verificar la protección');
}

// Ejecutar el script
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { setupBranchProtection, makeGitHubRequest };
