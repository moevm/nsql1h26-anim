import { useAuth } from "@contexts/index";
import styles from './Avatar.module.css';

export const Avatar = ({ 
  user: manualUser = null, 
  size = 40, 
  className = '' 
}) => {
  const { user: currentUser } = useAuth();
  const targetUser = manualUser || currentUser;
  if (!targetUser) {
    return (
      <div 
        className={`${styles.avatar} ${className}`} 
        style={{ width: size, height: size, backgroundColor: '#e2e8f0' }}
      />
    );
  }

  const {
    username = '',
    firstName = '',
    lastName = '',
    avatarUrl,
    avatarBackgroundColor = '#4a7c66'
  } = targetUser;

  const getInitials = () => {
    if (firstName && lastName) {
      return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
    }
    return username.slice(0, 2).toUpperCase() || '??';
  };

  const dynamicStyle = {
    width: size,
    height: size,
    minWidth: size,
    backgroundColor: avatarBackgroundColor,
    fontSize: `${size * 0.38}px`
  };

  return (
    <div className={`${styles.avatar} ${className}`} style={dynamicStyle}>
      {avatarUrl ? (
        <img 
          src={avatarUrl} 
          alt={username} 
          className={styles.image}
          onError={(e) => { e.target.style.display = 'none'; }}
        />
      ) : (
        <span className={styles.initials}>{getInitials()}</span>
      )}
    </div>
  );
};