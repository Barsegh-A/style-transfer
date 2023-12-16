import React, { useState } from 'react';
import { LoadingOutlined, InboxOutlined } from '@ant-design/icons';
import { message, Upload, Row, Col } from 'antd';

const { Dragger } = Upload

const getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
};

const beforeUpload = (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
        message.error('You can only upload JPG/PNG file!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
        message.error('Image must smaller than 2MB!');
    }
    return isJpgOrPng && isLt2M;
};

const ImageUpload = ({form}) => {
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState();

    const handleChange = (info) => {
        if (info.file.status === 'uploading') {
            setLoading(true);
            return;
        }
        if (info.file.status === 'done') {
            // Get this url from response in real world.
            getBase64(info.file.originFileObj, (url) => {
                setLoading(false);
                setImageUrl(url);
                form.setFieldsValue({ image: url });
            });
        }
    };

    const uploadButton = (
        <div>
            {loading ? <LoadingOutlined /> : <p className="ant-upload-drag-icon"><InboxOutlined /></p>}
            <p className="ant-upload-text" style={{padding: '20px'}}>Click or drag file to this area to upload</p>
        </div>
    );

    return (
            <Dragger
                name="avatar"
                listType="picture-card"
                showUploadList={false}
                customRequest={(file) => file.onSuccess()}
                beforeUpload={beforeUpload}
                onChange={handleChange}
                accept={'image/*'}
                style={{minWidth: 0}}
            >
                {imageUrl ? <img src={imageUrl} style={{ minWidth: 0, maxHeight: '400px', maxWidth: '400px' }} /> : uploadButton}
            </Dragger>
    );
};

export default ImageUpload;