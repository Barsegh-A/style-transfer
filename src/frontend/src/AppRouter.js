import React, { PureComponent } from 'react';
import ImageTransferForm from './components/ImageTransferForm';
import { Layout } from 'antd';

const { Content } = Layout;

class AppRouter extends PureComponent {

    render = () => (
        <>
            <Content style={{
                maxWidth: '1200px',
                margin: 'auto'
            }}>
                <ImageTransferForm />
            </Content>
        </>
    );
}

export default AppRouter;