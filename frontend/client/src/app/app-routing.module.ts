import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './component/home/home.component';
import { PredictComponent } from './component/predict/predict.component';
import { PageNotFoundComponent } from './Auth/page-not-found/page-not-found.component';
import { RegisterComponent } from './Auth/register/register.component';
import { LoginComponent } from './Auth/login/login.component';
import { ForgotPasswordComponent } from './Auth/forgot-password/forgot-password.component';
import { VerifyEmailComponent } from './Auth/verify-email/verify-email.component';

const routes: Routes = [
  {path:'', redirectTo :'home', pathMatch:'full'},
  {path: "home", component: HomeComponent},
  {path:'predict', component: PredictComponent},
  {path:'login', component: LoginComponent},
  {path:'register', component: RegisterComponent},
  {path:'forgot-password', component: ForgotPasswordComponent},
  {path:'verify-email', component: VerifyEmailComponent},
  {path:'**', component: PageNotFoundComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
