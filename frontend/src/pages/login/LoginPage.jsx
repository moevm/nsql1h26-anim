import { LuPawPrint } from "react-icons/lu";
import { AuthCard, AuthHeader, AuthFooter } from "@components/auth";
import { TextField } from "@components/ui/text-field";
import { Button } from "@components/ui/button";
import { useAuth } from "@contexts";
import { useForm } from "@hooks";

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

const initialState = {
  identifier: '',
  password: ''
}

export const LoginPage = () => {
  const { login } = useAuth()

  const [values, onChange] = useForm(initialState) 

  const onSubmit = async (event) => {
    event.preventDefault()
    try {
      await login(values)
    } catch (error) {
      alert(error)
    }
  }

  return (
    <div style={loginWrapper}>
      <AuthHeader
        icon={LuPawPrint}      
        title="Дикая природа"
        description="Сообщество наблюдателей дикой природы"
      />
      <AuthCard onSubmit={onSubmit}>
        <h2 style={title}>Вход</h2>
        <TextField 
          name="identifier"
          type="text"
          placeholder="your@email.com/username"
          label="email/username"
          value={values.identifier}
          onChange={onChange}
          autoComplete="identifier"
        />
        <TextField 
          name="password"
          type="password"
          placeholder="Введите ваш пароль" 
          label="пароль"
          value={values.password}
          onChange={onChange}
          autoComplete="current-password"
        />
        <Button type="submit">Войти</Button>
      </AuthCard>
      <AuthFooter
        title="Нет аккаунта?"
        link="Зарегистрироваться"
        to="/register"
      />
    </div>
  );
}