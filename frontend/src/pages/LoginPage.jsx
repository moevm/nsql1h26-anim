import { LuPawPrint } from "react-icons/lu";
import { AuthCard, AuthHeader, AuthFooter } from "../components/auth";
import { TextField } from "../components/ui/text-field";
import { Button } from "../components/ui/button";

const loginWrapper = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '12px',
  width: '100%',
  maxWidth: '420px',
  padding: '20px'
}

const title = {
  fontSize: '24px',
  fontWeight: '700'
}

export const LoginPage = () => {
  return (
    <div style={loginWrapper}>
      <AuthHeader
        icon={LuPawPrint}      
        title="Дикая природа"
        description="Сообщество наблюдателей дикой природы"
      />
      <AuthCard>
        <h2 style={title}>Вход</h2>
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
        <Button>Войти</Button>
      </AuthCard>
      <AuthFooter
        title="Нет аккаунта?"
        link="Зарегистрироваться"
        to="/register"
      />
    </div>
  );
}