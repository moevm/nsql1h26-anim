import { LuPawPrint } from "react-icons/lu";
import { AuthCard, AuthHeader, AuthFooter } from "../components/auth";
import { TextField } from "../components/ui/text-field";
import { Button } from "../components/ui/button";

const registerWrapper = {
  display: 'flex',
  flexDirection: 'column',
  gap: '12px',
  width: '100%',
  maxWidth: '420px',
  padding: '20px'
}

const title = {
  fontSize: '24px',
  fontWeight: '700'
}

export const RegisterPage = () => {
  return (
    <div style={registerWrapper}>
      <AuthHeader
        icon={LuPawPrint}      
        title="Дикая природа"
        description="Сообщество наблюдателей дикой природы"
      />
      <AuthCard>
        <h2 style={title}>Регистрация</h2>
        <TextField
          type="text"
          placeholder="@username"
          label="имя пользователя"
        />
        <TextField 
          type="email"
          placeholder="your@email.com"
          label="email"
        />
        <TextField 
          type="password"
          placeholder="Введите ваш пароль" 
          label="пароль"
        />
        <TextField 
          type="password"
          placeholder="Повторите пароль" 
          label="повторите пароль"
        />
        <Button>Создать аккаунт</Button>
      </AuthCard>
      <AuthFooter
        title="Уже есть аккаунт?"
        link="Войти"
        to="/login"
      />
    </div>
  );
}