export function validateUploadedFile(file: File) {
    const allowedFormats: string[] = ['mp3', 'wav'];
    const fileName: any = file.name;
    const fileExtension: string = fileName.split('.').pop().toLowerCase();
  
    if (!allowedFormats.includes(fileExtension)) {
      return false;
    }
  
    return true;
  }
  