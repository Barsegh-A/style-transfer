import React, { useState } from 'react';
import axios from 'axios';
import { Button, Form, Image, Col, Row } from 'antd';

import ImageUpload from "./ImageUpload";
import ImageList from "./ImageList";
import { API_ROOT } from "../config/env-vars";

import ReactCompareImage from 'react-compare-image';

const ImageTransferForm = () => {
    const [form] = Form.useForm();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [style, setStyle] = useState('Gorki');
    const [transferredImage, setTransferredImage] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [progress, setProgress] = useState(0);
    const [status, setStatus] = useState('');

    const onFinish = async (values) => {
        setIsModalOpen(true);
        setStatus('queued')
        const formData = {};

        Object.keys(values).forEach(key => {
            formData[key] = values[key];
        });

        formData['style'] = style
        setOriginalImage(formData['image']);

        const { data: job } = await axios.post(`${API_ROOT}/submit_job/`, formData, {
            mode: 'cors',
        });
        const intervalId = setInterval(async () => {
            const { data } = await axios.get(`${API_ROOT}/job?job_id=${job.id}`);
            const { status, image, progress } = data;
            //request to API
            if (status === 'finished') {
                setTransferredImage(image);
                clearInterval(intervalId);
            } else  if (status === 'failed') {
                clearInterval(intervalId);
            } else {
                setProgress(progress);
            }
            setStatus(status)
        }, 3000);

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    };

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };

    return (<>
        <h3>Here your photos meet the mastery of Armenian art!
            <br /><br />
            Discover a unique blend of tradition and innovation as we transform your images into captivating artworks, inspired by the distinct styles of Armenia's greatest painters. From the vibrant palettes of Martiros Saryan to the expressive brushstrokes of Minas Avetisyan, our app brings a touch of Armenian artistry to your cherished memories.
            <br /><br />
            Simply select the painter and upload your photo, and watch as we infuse it with the essence of Armenian art, creating a one-of-a-kind masterpiece that's both personal and steeped in cultural heritage. Whether you're an art aficionado or simply looking to add an artistic flair to your images, this platform is your gateway to experiencing the rich tapestry of Armenian art.
            <br /><br />
            Join us in celebrating the legacy of Armenian painters. Let's create something beautiful together!
        </h3>
        <Form
            name="basic"
            form={form}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            layout={'vertical'}
        >
            <Form.Item label="" name="style">
                <ImageList form={form} setStyle={setStyle} style={style} />
            </Form.Item>

            <Row>
                <Col span={9} order={3}>
                    <Form.Item
                        label={<span style={{ fontSize: '18px' }}>Result</span>}
                        style={{ fontSize: '18px', boxSizing: 'border-box', height: '400px' }}
                    >
                        {transferredImage ? <Image
                            style={{ maxHeight: '400px', maxWidth: '400px' }}
                            src={transferredImage} // Prefix with the correct MIME type
                        /> : null}

                    </Form.Item>
                </Col>
                <Col span={4} order={2}>
                    <Form.Item wrapperCol={{ offset: 0, span: 8 }}>
                        <Button
                            type="primary"
                            size='large'
                            htmlType="submit"
                            loading={status === 'queued' || status === 'processing'}
                            style={{ backgroundColor: '#001529', marginTop: '36px' }}
                        >
                            Submit {status == 'queued' ? "(Queued)" : null}
                        </Button>
                    </Form.Item>
                </Col>
                <Col span={9} order={1}>
                    <Row>
                        <Form.Item
                            name="image"
                            label={<span style={{ fontSize: '18px' }}>Your Photo</span>}
                            style={{ fontSize: '18px', boxSizing: 'border-box', height: '400px' }}
                        >
                            <ImageUpload form={form} />
                        </Form.Item>
                    </Row>
                </Col>
            </Row>
            {transferredImage ?
                <Row>
                    <Col span={22}>
                        <Form.Item
                            label={<span style={{ fontSize: '18px' }}>Side-by-side comparison</span>}
                            style={{ fontSize: '18px', boxSizing: 'border-box', height: '400px', padding: '100px' }}
                        >
                            <ReactCompareImage leftImage={originalImage} rightImage={transferredImage} />
                        </Form.Item>
                    </Col>
                </Row>
                : null}
        </Form>


        {/*<LoadingModal open={isModalOpen} progress={progress}/>*/}
    </>)
};

export default ImageTransferForm;