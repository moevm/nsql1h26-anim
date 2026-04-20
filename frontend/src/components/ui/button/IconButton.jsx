import styles from './IconButton.module.css'

export const IconButton = ({
  icon: Icon,
  text,
  className = '',
  ...props
}) => {
  return (
    <button className={`${styles.button} ${className}`} {...props}>
      <Icon className={styles.icon} />
      {text && <span className={styles.text}>{text}</span>}
    </button>
  )
}