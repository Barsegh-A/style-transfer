import React, {useState} from 'react';
import axios from 'axios';
import { Button, Form, Image } from 'antd';

import ImageUpload from "./ImageUpload";
import ImageList from "./ImageList";
import { API_ROOT } from "../config/env-vars";


const ImageTransferForm = () => {
    const [form] = Form.useForm();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [style, setStyle] = useState(null);
    const [transferredImage, setTransferredImage] = useState(null);
    const [progress, setProgress] = useState(0);
    const [status, setStatus] = useState('');

    const onFinish = async (values) => {
        setIsModalOpen(true);
        const formData = {};

        Object.keys(values).forEach(key => {
            formData[key] = values[key];
        });

        console.log(formData)

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
            } else {
                setProgress(progress);
            }
        }, 1000);

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
            <br/><br/>
            Discover a unique blend of tradition and innovation as we transform your images into captivating artworks, inspired by the distinct styles of Armenia's greatest painters. From the vibrant palettes of Martiros Saryan to the expressive brushstrokes of Minas Avetisyan, our app brings a touch of Armenian artistry to your cherished memories.
            <br/><br/>
            Simply select the painter and upload your photo, and watch as we infuse it with the essence of Armenian art, creating a one-of-a-kind masterpiece that's both personal and steeped in cultural heritage. Whether you're an art aficionado or simply looking to add an artistic flair to your images, this platform is your gateway to experiencing the rich tapestry of Armenian art.
            <br/><br/>
            Join us in celebrating the legacy of Armenian painters. Let's create something beautiful together!
        </h3>
        <Form
        name="basic"
        form={form}
        initialValues={{remember: true}}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
        layout={'vertical'}
    >
        <Form.Item
            label=""
            name="style"
            >
            <ImageList form={form}/>
        </Form.Item>

        <Form.Item
            name="image"
            label={<span style={{fontSize: '18px'}}>Your Photo</span>}
            style={{fontSize: '18px'}}
            >
            <ImageUpload form={form}/>
        </Form.Item>

        <Form.Item wrapperCol={{offset: 8, span: 16}}>
            <Button type="primary" size='large' htmlType="submit" loading={status==='processing'} style={{backgroundColor: '#001529'}}>
                Submit
            </Button>
        </Form.Item>
    </Form>
        {transferredImage ? <Image
            width={200} // Set the width as needed
            src={transferredImage} // Prefix with the correct MIME type
        /> : null}
    {/*<LoadingModal open={isModalOpen} progress={progress}/>*/}
    </>)
};

export default ImageTransferForm;