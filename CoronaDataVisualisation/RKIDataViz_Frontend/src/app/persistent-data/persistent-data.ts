import { HttpClient } from "@angular/common/http";
import { environment } from "../../environments/environment";

export function existInLocalStorage(key: string) {
  return localStorage.getItem(key) != null;
}

export function clearLocalStorage(http: HttpClient) {


  http.post(environment.PERSISTENT_DATA_CLEAR_PATH, { "delete": true }).subscribe(
    {
      next: (result: any) => {
        localStorage.clear();
        location.reload();
        },
      error:(error:any) => console.log(error)

      }
  );
  console.log("afterPost")
}
export function removeFromLocalStorage(key: string) {
  localStorage.removeItem(key);
}
export class persistentData<type>{

  data: type;
  key: string;


  constructor(data: type, key: string, func: any) {
    this.key = key;

    var str = localStorage.getItem(key);
    if (str == null) {
      this.data = data;
      localStorage.setItem(this.key, JSON.stringify(data));
    } else {
      this.data = JSON.parse(str)
    }

    addEventListener("storage", (event: StorageEvent) => {
      if (event.key == key && event.newValue != null) {
        if (event.newValue != event.oldValue)
          this.data = JSON.parse(event.newValue)
        func(this.data);
      }
    });

  }

  removeFromStorage() {
    localStorage.removeItem(this.key);
  }

  get() {
    return this.data;
  }

  set(data: type) {
    this.data = data;
    localStorage.setItem(this.key, JSON.stringify(data));


  }

  update() {
    localStorage.setItem(this.key, JSON.stringify(this.data));
  }

}
