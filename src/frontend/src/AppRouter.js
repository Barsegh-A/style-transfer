import React, { PureComponent } from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import MainHeader from './components/MainHeader';
import ImageTransferForm from './components/ImageTransferForm';
import { Layout, Menu } from 'antd';

const { Header, Content } = Layout;

class AppRouter extends PureComponent {

    render = () => (
        <>
            <MainHeader />
            <Content style={{
                padding: '50px 200px',
                // backgroundImage: "url('https://i.ibb.co/tZSRH3D/output-onlinepngtools-1.png')",
                // backgroundPosition: 'cover',
                // backgroundRepeat: 'repeat',
                // backgroundAttachment: 'fixed',
            }}>
                <ImageTransferForm />
            </Content>
        </>
    );
}

export default AppRouter;