import { Component, OnInit } from '@angular/core';

declare const L: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  title = 'locationApp';

  treename="Maple";
  treetype="Deciduous";
  final: any[] = [];
  public latitute1;
  submit=false;
  date;
  time;
  val: string = '';
  lati: number = 0;
  longi: number = 0;


 
  onSubmit(value:any)
  {
    console.log(value);
    this.submit=true;
    setTimeout(() => {
      this.submit=false;
    }, 3000);
  }

  ngOnInit() {
    if (!navigator.geolocation) {
      console.log('location is not supported');
    }
    navigator.geolocation.getCurrentPosition((position) => {
      const coords = position.coords;
      const latLong = [coords.latitude, coords.longitude];
      this.lati=coords.latitude;
      this.longi=coords.longitude;
      this.final.push(this.lati,this.longi);
      console.log(
        `lat: ${position.coords.latitude}, lon: ${position.coords.longitude}`
      );
     


     
    });
    
  }
  geturl()
  {
    return "url('assets/edu.jpg')";
  }

  
}