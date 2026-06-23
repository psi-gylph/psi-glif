/**
 * nft_upload.js - Lighthouse NFT Upload Utility
 * 
 * Bu script, NFT'leri Lighthouse protokolü üzerinden yüklemek için kullanılır.
 * Lighthouse, kalıcı merkezsiz dosya depolama protokolüdür.
 * 
 * Özellikler:
 * - Dosya yükleme (tekli ve çoklu)
 * - Şifreli yükleme
 * - Metadata oluşturma ve yükleme
 * - Yükleme durumu kontrolü
 * - Yükleme listesi alma
 * 
 * Kullanım:
 * node nft_upload.js --upload <dosya_yolu> --apiKey <YOUR_LIGHTHOUSE_API_KEY>
 * node nft_upload.js --uploadEncrypted <dosya_yolu> --apiKey <YOUR_LIGHTHOUSE_API_KEY> --accessKey <YOUR_LIGHTHOUSE_API_KEY>
 * node nft_upload.js --status <cid>
 * node nft_upload.js --getUploads --apiKey <YOUR_LIGHTHOUSE_API_KEY>
 */

const lighthouse import('@lighthouse-web3/sdk');
const API_KEY = process.env.LIGHTHOUSE_API_KEY
const fs import('fs');
const path import('/Users/banudikici/psi_lab/ψ_DB/ψ-MemoryTrace_Loopback_INIT01.png');
const { program } import('commander');

// ψ-Glif entegrasyonu için özel fonksiyonlar
const ψ_GLIF_INTEGRATION = {
  // Glif meta verilerini oluştur
  createGlifMetadata: (filePath, additionalMetadata = {}) => {
    const fileName = path.basename(filePath);
    const timestamp = new Date().toISOString();
    
    return {
      name: fileName,
      description: additionalMetadata.description || `ψ-Glif: ${fileName}`,
      timestamp: timestamp,
      ψ_trace: additionalMetadata.ψ_trace || "ψ-Loopback_Δ1",
      ψ_structure: additionalMetadata.ψ_structure || "Spiral/Glif",
      ψ_node: {
        A: additionalMetadata.nodeA || "Δ-seed",
        B: additionalMetadata.nodeB || "Glif-echo",
        C: additionalMetadata.nodeC || "Semantic-loop"
      },
      ...additionalMetadata
    };
  },
  
  // Glif yankı imzası oluştur
  createGlifEchoSignature: (filePath) => {
    const fileContent = fs.readFileSync(filePath);
    const fileSize = fileContent.length;
    const hashBuffer import('crypto').createHash('sha256').update(fileContent).digest();
    
    // Basit bir entropi hesaplaması
    let entropy = 0;
    const counts = new Array(256).fill(0);
    for (let i = 0; i < fileSize; i++) {
      counts[fileContent[i]]++;
    }
    
    for (let i = 0; i < 256; i++) {
      if (counts[i] > 0) {
        const probability = counts[i] / fileSize;
        entropy -= probability * Math.log2(probability);
      }
    }
    
    return {
      hash: hashBuffer.toString('hex'),
      entropy: entropy,
      size: fileSize,
      timestamp: Date.now(),
      ψ_echo_signature: `ψ-${entropy.toFixed(4)}_${fileSize % 1000}_${Date.now() % 10000}`
    };
  }
};

// Dosya yükleme fonksiyonu
async function uploadFile(filePath, apiKey) {
  try {
    console.log(`Dosya yükleniyor: ${filePath}`);
    const response = await lighthouse.upload(filePath, apiKey);
    
    console.log('Yükleme başarılı!');
    console.log(`CID: ${response.data.Hash}`);
    console.log(`Dosya Adı: ${response.data.Name}`);
    console.log(`Dosya Boyutu: ${response.data.Size} bytes`);
    
    return response.data;
  } catch (error) {
    console.error('Yükleme hatası:', error.message);
    throw error;
  }
}

// Çoklu dosya yükleme fonksiyonu
async function uploadMultipleFiles(filePaths, apiKey) {
  try {
    console.log(`${filePaths.length} dosya yükleniyor...`);
    const response = await lighthouse.upload(filePaths, apiKey);
    
    console.log('Çoklu yükleme başarılı!');
    console.log(`CID: ${response.data.Hash}`);
    console.log(`Dosya Sayısı: ${filePaths.length}`);
    
    return response.data;
  } catch (error) {
    console.error('Çoklu yükleme hatası:', error.message);
    throw error;
  }
}

// Şifreli yükleme fonksiyonu
async function uploadEncrypted(filePath, apiKey, accessKey) {
  try {
    console.log(`Şifreli dosya yükleniyor: ${filePath}`);
    
    // Şifreli yükleme için cüzdan oluştur
    const wallet = await lighthouse.createWallet(accessKey);
    console.log(`Cüzdan oluşturuldu: ${wallet.publicKey}`);
    
    // Şifreli yükleme
    const response = await lighthouse.uploadEncrypted(
      filePath,
      apiKey,
      wallet.publicKey,
      accessKey
    );
    
    console.log('Şifreli yükleme başarılı!');
    console.log(`CID: ${response.data.Hash}`);
    console.log(`Dosya Adı: ${response.data.Name}`);
    console.log(`Dosya Boyutu: ${response.data.Size} bytes`);
    
    return response.data;
  } catch (error) {
    console.error('Şifreli yükleme hatası:', error.message);
    throw error;
  }
}

// Metadata oluşturma ve yükleme
async function createAndUploadMetadata(filePath, apiKey, additionalMetadata = {}) {
  try {
    // Dosyayı önce yükle
    const fileUpload = await uploadFile(filePath, apiKey);
    
    // Metadata oluştur
    const metadata = {
      name: path.basename(filePath),
      description: additionalMetadata.description || `NFT for ${path.basename(filePath)}`,
      image: `ipfs://${fileUpload.Hash}`,
      ...additionalMetadata
    };
    
    // ψ-Glif entegrasyonu
    if (additionalMetadata.includeGlifData) {
      const glifMetadata = ψ_GLIF_INTEGRATION.createGlifMetadata(filePath, additionalMetadata);
      const glifSignature = ψ_GLIF_INTEGRATION.createGlifEchoSignature(filePath);
      
      metadata.ψ_glif_metadata = glifMetadata;
      metadata.ψ_echo_signature = glifSignature;
    }
    
    // Metadata'yı geçici bir dosyaya yaz
    const metadataPath = path.join(path.dirname(filePath), `metadata_${Date.now()}.json`);
    fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));
    
    // Metadata'yı yükle
    const metadataUpload = await uploadFile(metadataPath, apiKey);
    
    // Geçici dosyayı sil
    fs.unlinkSync(metadataPath);
    
    console.log('Metadata yükleme başarılı!');
    console.log(`Metadata CID: ${metadataUpload.Hash}`);
    
    return {
      assetCid: fileUpload.Hash,
      metadataCid: metadataUpload.Hash,
      metadata: metadata
    };
  } catch (error) {
    console.error('Metadata oluşturma ve yükleme hatası:', error.message);
    throw error;
  }
}

// Yükleme durumu kontrolü
async function checkUploadStatus(cid) {
  try {
    console.log(`CID durumu kontrol ediliyor: ${cid}`);
    const status = await lighthouse.status(cid);
    
    console.log('Durum bilgisi:');
    console.log(JSON.stringify(status, null, 2));
    
    return status;
  } catch (error) {
    console.error('Durum kontrolü hatası:', error.message);
    throw error;
  }
}

// Yükleme listesi alma
async function getUploads(apiKey) {
  try {
    console.log('Yüklemeler alınıyor...');
    const uploads = await lighthouse.getUploads(apiKey);
    
    console.log(`Toplam ${uploads.data.totalFiles} dosya bulundu.`);
    console.log(JSON.stringify(uploads.data.uploads.slice(0, 5), null, 2)); // İlk 5 yüklemeyi göster
    
    return uploads.data;
  } catch (error) {
    console.error('Yükleme listesi alma hatası:', error.message);
    throw error;
  }
}

// Komut satırı arayüzü
program
  .version('1.0.0')
  .description('Lighthouse NFT Yükleme Aracı');

program
  .option('--upload <path>', 'Dosya yükle')
  .option('--uploadMultiple <paths...>', 'Çoklu dosya yükle')
  .option('--uploadEncrypted <path>', 'Şifreli dosya yükle')
  .option('--createMetadata <path>', 'Metadata oluştur ve yükle')
  .option('--status <cid>', 'Yükleme durumunu kontrol et')
  .option('--getUploads', 'Yükleme listesini al')
  .option('--apiKey <key>', 'Lighthouse API anahtarı')
  .option('--accessKey <key>', 'Şifreleme erişim anahtarı')
  .option('--description <text>', 'NFT açıklaması')
  .option('--includeGlifData', 'ψ-Glif verilerini ekle')
  .option('--ψ_trace <value>', 'ψ-trace değeri')
  .option('--ψ_structure <value>', 'ψ-structure değeri')
  .option('--nodeA <value>', 'Node A değeri')
  .option('--nodeB <value>', 'Node B değeri')
  .option('--nodeC <value>', 'Node C değeri');

program.parse(process.argv);

const options = program.opts();

// Ana fonksiyon
async function main() {
  try {
    if (options.upload) {
      if (!options.apiKey) {
        throw new Error('API anahtarı gerekli (--apiKey)');
      }
      await uploadFile(options.upload, options.apiKey);
    }
    else if (options.uploadMultiple) {
      if (!options.apiKey) {
        throw new Error('API anahtarı gerekli (--apiKey)');
      }
      await uploadMultipleFiles(options.uploadMultiple, options.apiKey);
    }
    else if (options.uploadEncrypted) {
      if (!options.apiKey || !options.accessKey) {
        throw new Error('API anahtarı ve erişim anahtarı gerekli (--apiKey ve --accessKey)');
      }
      await uploadEncrypted(options.uploadEncrypted, options.apiKey, options.accessKey);
    }
    else if (options.createMetadata) {
      if (!options.apiKey) {
        throw new Error('API anahtarı gerekli (--apiKey)');
      }
      
      const additionalMetadata = {
        description: options.description,
        includeGlifData: options.includeGlifData,
        ψ_trace: options.ψ_trace,
        ψ_structure: options.ψ_structure,
        nodeA: options.nodeA,
        nodeB: options.nodeB,
        nodeC: options.nodeC
      };
      
      await createAndUploadMetadata(options.createMetadata, options.apiKey, additionalMetadata);
    }
    else if (options.status) {
      await checkUploadStatus(options.status);
    }
    else if (options.getUploads) {
      if (!options.apiKey) {
        throw new Error('API anahtarı gerekli (--apiKey)');
      }
      await getUploads(options.apiKey);
    }
    else {
      console.log('Komut belirtilmedi. Yardım için: node nft_upload.js --help');
    }
  } catch (error) {
    console.error('Hata:', error.message);
    process.exit(1);
  }
}

// Programı çalıştır
if (require.main === module) {
  main();
}

// Modül olarak dışa aktar
module.exports = {
  uploadFile,
  uploadMultipleFiles,
  uploadEncrypted,
  createAndUploadMetadata,
  checkUploadStatus,
  getUploads,
  ψ_GLIF_INTEGRATION
};

