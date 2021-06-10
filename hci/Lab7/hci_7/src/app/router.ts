import { Routes,CanActivate } from '@angular/router';
import { AppComponent } from './app.component';
import { FrontComponent } from './front/front.component';
import { BackComponent } from './back/back.component';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';
import { HomeComponent } from './home/home.component';
import { RowComponent } from './row/row.component';
const route: Routes = [

    {
        path:'',
        component:HomeComponent
    },
    {
        path:'front',
        component:FrontComponent
    },
    {
        path:'row',
        component:RowComponent
    },
    {
        path:'back',
        component:BackComponent
    },
    {
        path:'home',
        component:HomeComponent
    },
    {
        path:'**',
        component:PagenotfoundComponent
    }
    
    
  
];
export default route;