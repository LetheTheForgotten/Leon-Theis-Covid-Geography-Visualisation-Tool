import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export function existInLocalStorage(key: string) {
  return localStorage.getItem(key) != null;
}

export function removeFromLocalStorage(key: string) {
  localStorage.removeItem(key);
}
export class persistentObject<type extends object>{

  data: type;
  key: string;
  http: HttpClient;
  broadcast: BroadcastChannel

  constructor(data: type, key: string, func: any, http: HttpClient) {
    localStorage.setItem(key,"placeholder")

    this.key = key;
    this.http = http;
    this.data = data;
    this.broadcast = new BroadcastChannel(key)
    this.http.get<type>(environment.PERSISTENT_DATA_PATH + key).subscribe(
      {
        next: (result) => {
          this.data = result;
          func(this.data)
        },
        error: (error) => {
          if (error.status == 404) {
            this.set(data);
          }
          else {
            console.log(error)
          }
        }
      }

    );


    this.broadcast.onmessage = (event: MessageEvent<any>) => {
      this.http.get<type>(environment.PERSISTENT_DATA_PATH + key).subscribe(
        {
          next: (result) => {
            this.data = result;
            func(this.data);
          },
          error: (error) => console.log(error)
        }

      );

    };

    //addEventListener("storage", (event: StorageEvent) => {
    //  if (event.key == null) {
    //    localStorage.setItem(key, "placeholder")
    //    this.http.get<type>(environment.PERSISTENT_DATA_PATH + key).subscribe(
    //      {
    //        next: (result) => {
    //          this.data = result;

    //          func(this.data);
    //        },
    //        error: (error) => console.log(error)
    //      }

    //    );
    //  }
    //}

    //);

  }

  removeFromStorage() {
    //not implemented
  }

  get() {
    return this.data;
  }

  set(data: type) {
    this.data = data;

    this.http.post(environment.PERSISTENT_DATA_PATH + this.key, data).subscribe(
      {
        next:(result)=> this.broadcast.postMessage("reload"),
        error: (error) => console.log(error)
      });

    


  }

  update() {
    this.set(this.data);
  }

}

