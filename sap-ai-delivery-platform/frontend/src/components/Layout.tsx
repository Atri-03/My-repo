import { makeStyles, tokens, Title3 } from '@fluentui/react-components';
import { NavLink, Outlet } from 'react-router-dom';
import { navItems } from './navItems';

const useStyles = makeStyles({
  root: {
    display: 'flex',
    minHeight: '100vh',
  },
  sidebar: {
    width: '260px',
    flexShrink: 0,
    backgroundColor: tokens.colorNeutralBackground2,
    borderRight: `1px solid ${tokens.colorNeutralStroke2}`,
    padding: '16px 8px',
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  brand: {
    padding: '8px 12px 16px 12px',
  },
  link: {
    display: 'block',
    padding: '8px 12px',
    borderRadius: tokens.borderRadiusMedium,
    color: tokens.colorNeutralForeground1,
    textDecoration: 'none',
    fontSize: tokens.fontSizeBase300,
  },
  activeLink: {
    backgroundColor: tokens.colorBrandBackground2,
    color: tokens.colorBrandForeground2,
    fontWeight: tokens.fontWeightSemibold,
  },
  content: {
    flexGrow: 1,
    padding: '24px 32px',
    overflowY: 'auto',
  },
});

/** Application shell: left navigation rail + routed page content. */
export function Layout() {
  const styles = useStyles();
  return (
    <div className={styles.root}>
      <nav className={styles.sidebar} aria-label="Main navigation">
        <div className={styles.brand}>
          <Title3>SAP AI Delivery Platform</Title3>
        </div>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `${styles.link} ${isActive ? styles.activeLink : ''}`}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
