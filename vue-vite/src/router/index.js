import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import BlogDetails from '../views/BlogDetails.vue'
import BlogEdit from '../views/BlogEdit.vue'
import Blogs from '../views/Blogs.vue'

const routes = [
    {
        path: '/',
        name: 'Index',
        meta: {
                reqireAuth: true
            },
        redirect: { name: 'Blogs' }
        },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/blogs',
        name: 'Blogs',
        component: Blogs
    },
    {
        path: '/blog/add',
        name: 'BlogAdd',
        meta: {
            reqireAuth: true
        },
        component: BlogEdit
    },
    {
        path: '/blog/:blogId',
        name: 'BlogDetail',
        component: BlogDetails
    },
    {
        path: '/blog/:blodId/edit',
        name: 'BlogEdit',
        meta: {
            requireAuth: true
        },
        component: BlogEdit
    }
]

const router = createRouter(
    {
        history: createWebHistory(),
        routes: routes,
    }
)

export default router