import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-back',
  templateUrl: './back.component.html',
  styleUrls: ['./back.component.css']
})
export class BackComponent implements OnInit {

  issubmit=false;
  val1
  val2
  val3
  val4
  val5
  val6
  val7
  val8
  val9
  val10
  val11
  val12
  score=0;
  correct=0;
  incorrect=0;
  


  constructor() { }

  ngOnInit(): void {
    this.issubmit=false;

  }

  onSubmit(value:any)
  {
    this.correct=0;
    this.incorrect=0;
    console.log(value);
    if(this.val1=='J')
    {
       this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val2=='A')
    {
       this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val3=='C')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val4=='K')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val5=='R')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val6=='U')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val7=='B')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val8=='Y')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val9=='L')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val10=='E')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val11=='V')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    if(this.val12=='I')
    {
      this.correct+=1;
    }
    else{
      this.incorrect+=1
    }
    
    this.score=this.correct-this.incorrect;
    this.issubmit=true;
    setTimeout(() => {
      this.issubmit=false;
    }, 3000);


  }

}
