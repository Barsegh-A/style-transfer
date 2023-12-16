import React from 'react';
import { List, Card } from 'antd';

const data = [
    {
        title: 'Arshile Gorky',
        value: 'Gorki',
        image: 'https://upload.wikimedia.org/wikipedia/commons/0/0d/%22Agony%22_by_Arshile_Gorky.jpg'
    },
    {
        title: 'Hovhannes Aivazovsky',
        value: 'Aivazovsky',
        image: 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg'
    },
    {
        title: 'Martiros Saryan',
        value: 'Saryan',
        image: 'https://uploads0.wikiart.org/images/martiros-saryan/mottled-landscape-1924.jpg!Large.jpg'
    },
    {
        title: 'Minas Avetisyan',
        value: 'Minas',
        image: 'https://media.sketchfab.com/models/8507f4b42fa64460b161141ad8bdafb1/thumbnails/26b4374259e84b0e909613341d420e61/d1d87ccff4b2494dabbf55da324146d6.jpeg'
    },
    {
        title: 'Vardges Surenyants',
        value: 'Sureniants',
        image: 'https://upload.wikimedia.org/wikipedia/commons/e/ec/Shamiram_ara.jpeg'
    },
];

const ImageList = ({ form, style, setStyle }) => {
    const handleClick = (item) => {
        form.setFieldsValue({ style: item.value });
        setStyle(item.value);
    }
    return (
        <>
            <List
                grid={{gutter: 5}}
                dataSource={data}
                renderItem={(item) => (
                    <List.Item onClick={() => handleClick(item)} style={{cursor: 'pointer'}}>
                        <Card
                            title={item.title}
                            size={'large'}
                            style={{
                                backgroundColor: (item.value === style ? '#eee' : 'transparent'),
                                borderColor: '#001529',
                            }}
                            bodyStyle={{
                                padding: '6px 20px'
                            }}
                        >
                            <img src={item.image} alt={item.title} style={{ width: '170px', height: '80px' }} />
                        </Card>
                    </List.Item>
                )}
            />
        </>
    )
};

export default ImageList;