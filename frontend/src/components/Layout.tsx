import CreateDataSet from '@/components/CreateDataSet'
import bellIcon from '@/assets/icons/bell-icon.svg'

const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="navbar px-8">
        <div className="navbar-start">
          <span className="normal-case text-xl">AudioMosaic</span>
        </div>
        <div className="navbar-end">
          <button className="btn btn-circle">
            <div className="indicator">
              <img className="w-6" src={bellIcon} alt="bell icon" />
              <span className="badge badge-xs badge-primary indicator-item"></span>
            </div>
          </button>
        </div>
      </div>
      <main className="flex-grow">
        <CreateDataSet />
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