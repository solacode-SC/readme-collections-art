export class ImageLoader {
  private static cache = new Map<string, HTMLImageElement>();
  private static cropCache = new Map<string, string>();

  static async loadImage(src: string): Promise<HTMLImageElement> {
    if (this.cache.has(src)) {
      return this.cache.get(src)!;
    }
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        this.cache.set(src, img);
        resolve(img);
      };
      img.onerror = (e) => reject(new Error(`Failed to load image at ${src}: ${e}`));
      img.src = src;
    });
  }

  static cropToDataUrl(
    img: HTMLImageElement,
    box: [number, number, number, number],
    size: [number, number],
    quality: number = 0.92
  ): string {
    const key = `${img.src}_${box.join(",")}_${size.join(",")}_${quality}`;
    if (this.cropCache.has(key)) {
      return this.cropCache.get(key)!;
    }

    const [bx0, by0, bx1, by1] = box;
    const bw = bx1 - bx0;
    const bh = by1 - by0;
    const [sw, sh] = size;

    const canvas = document.createElement("canvas");
    canvas.width = sw;
    canvas.height = sh;
    const ctx = canvas.getContext("2d");
    if (!ctx) return "";

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(img, bx0, by0, bw, bh, 0, 0, sw, sh);

    const dataUrl = canvas.toDataURL("image/jpeg", quality);
    this.cropCache.set(key, dataUrl);
    return dataUrl;
  }
}
