import bellIcon from '@/assets/icons/bell-icon.svg';
import RoutesList from '@/routes';
import { Link } from 'react-router-dom';

const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="navbar px-8">
        <div className="navbar-start">
          <img src="/favicon.png" width="55px" alt="" />
          <span className="normal-case text-xl ml-4">
            <Link to="/">AudioMosaic</Link>
          </span>
        </div>
        <div className="navbar-end gap-8">
          <Link to="/create">Create a Dataset</Link>
          <button className="btn btn-circle">
            <div className="indicator">
              <img className="w-6" src={bellIcon} alt="bell icon" />
              <span className="badge badge-xs badge-primary indicator-item"></span>
            </div>
          </button>
        </div>
      </div>
      <main className="flex-grow">
        <RoutesList />
      </main>
      <footer className="footer footer-center p-4 bg-base-300 text-base-content">
        <div>
          <p>Copyright © 2023</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout