import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-front',
  templateUrl: './front.component.html',
  styleUrls: ['./front.component.css']
})
export class FrontComponent implements OnInit {

  constructor(private router:Router) { }

  ngOnInit(): void {
    setTimeout(() => {
      this.router.navigate(['back']);
    }, 12000);
    
    var timeleft = 10;
    var downloadTimer = setInterval(function()
    {
    if(timeleft <= 0)
    {
      clearInterval(downloadTimer);
      document.getElementById("countdown").innerHTML = "Finished";
      console.log("hello");
      
    } 
    else 
    {
      document.getElementById("countdown").innerHTML = timeleft + " seconds remaining";
    }
     timeleft -= 1;
    }, 1000);

  
    
  
  }

}