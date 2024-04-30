export class persistentMap<Key, Value>{

  data: Map<Key, Value>;
  key: string;


  constructor(data: Map<Key, Value>, key: string, func: any) {
    this.key = key;

    var str = localStorage.getItem(key);
    if (str == null) {
      this.data = data;
      localStorage.setItem(this.key, JSON.stringify([...data]))
    } else {
      try {
        this.data = new Map<Key, Value>(JSON.parse(str));
      }
      catch {
        this.data = data;
        localStorage.setItem(this.key, JSON.stringify([...data]))
      }
      

    }

    addEventListener("storage", (event: StorageEvent) => {
      if (event.key == key && event.newValue != null) {
        if (event.newValue != event.oldValue) {
          this.data = new Map<Key, Value>(JSON.parse(event.newValue));

          func(this.data);
        }
      }
    });

  }

  removeFromStorage() {
    localStorage.removeItem(this.key);
  }

  get() {
    return this.data;
  }

  set(data: Map<Key, Value>) {
    this.data = data;
    localStorage.setItem(this.key, JSON.stringify([...this.data]))
  }

  update() {
    localStorage.setItem(this.key, JSON.stringify([...this.data]))
  }

}

