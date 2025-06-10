import React from 'react';
import { Layout, Menu } from 'antd';
import { 
  DashboardOutlined,
  TeamOutlined,
  DollarOutlined,
  BarChartOutlined,
  MailOutlined
} from '@ant-design/icons';
import Link from 'next/link';

const { Header, Content, Sider } = Layout;

export const MainLayout: React.FC = ({ children }) => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible>
        <div className="logo" />
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<DashboardOutlined />}>
            <Link href="/">Dashboard</Link>
          </Menu.Item>
          <Menu.Item key="2" icon={<TeamOutlined />}>
            <Link href="/crm-dashboard">CRM</Link>
          </Menu.Item>
          <Menu.Item key="3" icon={<DollarOutlined />}>
            <Link href="/financial">Financial</Link>
          </Menu.Item>
          <Menu.Item key="4" icon={<BarChartOutlined />}>
            <Link href="/analytics">Analytics</Link>
          </Menu.Item>
          <Menu.Item key="5" icon={<MailOutlined />}>
            <Link href="/email-assistant">Email Assistant</Link>
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};
