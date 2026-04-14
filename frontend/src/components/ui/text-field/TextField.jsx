import { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import styles from './TextField.module.css';

export const TextField = ({
  label,
  icon: Icon,
  type = 'text',
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === 'password';
  const inputType = isPassword 
    ? (showPassword ? 'text' : 'password')
    : type;

  const handleShowPassword = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className={styles.field}>
      {label && <label className={styles.label}>{label}</label>}
      <div className={styles.inputWrapper}>
        {Icon && <Icon className={styles.icon} />}
        <input
          type={inputType}
          className={styles.input}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            className={styles.eyeButton}
            onClick={handleShowPassword}
            tabIndex={-1}
          >  
            {showPassword 
              ? <FiEyeOff/>
              : <FiEye/>
            }
          </button>
        )}
      </div>
    </div>
  );
};