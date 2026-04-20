import { LuPawPrint } from "react-icons/lu";
import { AuthCard, AuthHeader, AuthFooter } from "../../components/auth";
import { TextField } from "../../components/ui/text-field";
import { Button } from "../../components/ui/button";
import { request } from "../../api/axios";
import { useAuth } from "../../contexts";
import { useForm } from "../../hooks";

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

const initialState = {
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  repeatPassword: ''
}

export const RegisterPage = () => {
  const [values, onChange] = useForm(initialState)
  const { login } = useAuth()

  const onSubmit = async (e) => {
    e.preventDefault()
    if (values.password !== values.repeatPassword) {
      alert('Пароли не совпадают!')
      return
    }

    const { repeatPassword, ...registerData} = values

    try {
      await request('post', '/auth/register', registerData)
      const loginCredentials = {
        identifier: registerData.email,
        password: registerData.password
      }
      await login(loginCredentials)
    } catch (error) {
      console.error(error)      
    }
  }

  return (
    <div style={registerWrapper}>
      <AuthHeader
        icon={LuPawPrint}      
        title="Дикая природа"
        description="Сообщество наблюдателей дикой природы"
      />
      <AuthCard onSubmit={onSubmit}>
        <h2 style={title}>Регистрация</h2>
        <TextField
          name="username"
          type="text"
          placeholder="@username"
          label="имя пользователя"
          value={values.username}
          onChange={onChange}
          autoComplete="username"
        />
        <TextField 
          name="email"
          type="email"
          placeholder="your@email.com"
          label="email"
          value={values.email}
          onChange={onChange}
          autoComplete="email"
        />
        <TextField
          name="firstName"
          type="text"
          placeholder="Введите своё имя"
          label="имя"
          value={values.firstName}
          onChange={onChange}
          autoComplete="given-name"
        />
        <TextField 
          name="lastName"
          type="text"
          placeholder="Введите свою фамилию"
          label="фамилия"
          value={values.lastName}
          onChange={onChange}
          autoComplete="family-name"
        />
        <TextField 
          name="password"
          type="password"
          placeholder="Введите ваш пароль" 
          label="пароль"
          value={values.password}
          onChange={onChange}
          autoComplete="new-password"
        />
        <TextField 
          name="repeatPassword"
          type="password"
          placeholder="Повторите пароль" 
          label="повторите пароль"
          value={values.repeatPassword}
          onChange={onChange}
          autoComplete="new-password"
        />
        <Button type="submit">Создать аккаунт</Button>
      </AuthCard>
      <AuthFooter
        title="Уже есть аккаунт?"
        link="Войти"
        to="/login"
      />
    </div>
  );
}