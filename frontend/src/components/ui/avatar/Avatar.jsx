import styles from './Avatar.module.css';

export const Avatar = ({ 
  firstName, 
  lastName, 
  image = null, 
  backgroundColor = '#4a90e2',
  size = 40 
}) => {
  const initials = `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  
  const dynamicStyle = {
    width: `${size}px`,
    height: `${size}px`,
    backgroundColor,
    fontSize: `${size * 0.4}px`
  };

  return (
    <div className={styles.avatar} style={dynamicStyle}>
      {image ? (
        <img 
          src={image} 
          alt={initials} 
          className={styles.image}
        />
      ) : (
        <span>{initials}</span>
      )}
    </div>
  );
};