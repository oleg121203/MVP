export class Logger {
  private context: string;

  constructor(context: string) {
    this.context = context;
  }

  log(message: string, ...args: any[]) {
    console.log(`[${this.context}][LOG] ${message}`, ...args);
  }

  error(message: string, ...args: any[]) {
    console.error(`[${this.context}][ERROR] ${message}`, ...args);
  }

  warn(message: string, ...args: any[]) {
    console.warn(`[${this.context}][WARN] ${message}`, ...args);
  }

  info(message: string, ...args: any[]) {
    console.info(`[${this.context}][INFO] ${message}`, ...args);
  }
}
