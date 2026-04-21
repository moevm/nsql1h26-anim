import { Dropdown } from '@components/ui/dropdown';
import { FaUser, FaSignOutAlt, FaFileExport } from 'react-icons/fa'
import styles from './Header.module.css';
import { useAuth } from '@contexts/index';

export const Header = () => {
  const { logout } = useAuth()
  const menuItems = [
      // { 
      //   to: '/profile', 
      //   label: 'Мой профиль', 
      //   icon: <FaUser /> 
      // },
      // { 
      //   to: '/export', 
      //   label: 'Экспорт JSON', 
      //   icon: <FaFileExport /> 
      // },
      { 
        to: '/logout', 
        label: 'Выйти', 
        icon: <FaSignOutAlt />,
        onClick: logout
      }
    ]
  return (
    <header className={styles.headerExternal}>
      <div className={styles.headerInternal}>
        <div className={styles.headerContent}>
          <div className={styles.logoArea}>
            <h1>WildLife</h1>
          </div>
          <nav className={styles.navLinks}>
            <span className={`${styles.navItem} ${styles.active}`}>Лента</span>
            <span className={styles.navItem}>Профиль</span>
          </nav>
          <Dropdown 
            trigger="Профиль"
            items={menuItems}
            position="bottom"
          />
        </div>
      </div>
    </header>
  );
};
