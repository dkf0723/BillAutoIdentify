import Home from "./Home/Home-index"
import Test from "./test"
import Search from "./Search/Search-index"
import OutAndRevise from "./OutAndRevise/OutAndRevise-index"
import Account from "./Account/Account-index"
import Login from "./Login/Login-index"
import { Link } from "react-router-dom"
import Signup from "./Signup/Signup-index"
import ChangePswd from "./Password/ChangePswd-index"
import MediaUpload from "./Media/MediaUpload"
//常駐菜單列切換頁面
export const routeConfig = [
    {
        path: '/',
        element: <Home />,
    },
    { path: '/test', element: <Test /> },
    { path: '/Search', element: <Search /> },
    { path: '/OutAndRevise', element: <OutAndRevise /> },
    { path: '/Media', element: <MediaUpload /> },
    { path: '/Account', element: <Account /> },
    { path: '/Login', element: <Login /> },
    { path: '/Signup', element: <Signup /> },
    { path: '/Password', element: <ChangePswd /> },
    
    
   
]