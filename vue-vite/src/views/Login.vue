<template>
    <v-card>
        <v-layout>
            <v-app-bar color="primary" density="compact">
                <template v-slot:prepend>
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                </template>

                <v-app-bar-title>Login</v-app-bar-title>

            </v-app-bar>

            <v-main>
                <v-form ref="ruleForm" v-model="valid" lazy-validation>
                    <v-container>
                        <v-row justify="space-between">
                            <v-col cols="12" md="4">
                                <v-text-field v-model="ruleForm.username" :rules="nameRule" :counter="20"
                                    label="First name" required></v-text-field>
                            </v-col>

                            <v-col cols="12" md="4">
                                <v-text-field v-model="ruleForm.password" :rules="passwordRule" :counter="20"
                                    label="Last name" required></v-text-field>
                            </v-col>

                        </v-row>
                        <v-btn :disabled="!valid" color="success" class="mr-4" @click="login">
                            Login
                        </v-btn>
                        <v-btn color="error" class="mr-4" @click="reset">
                            Reset
                        </v-btn>
                        <p v-if="valid">True</p>
                        <p v-else>False</p>
                    </v-container>
                </v-form>
            </v-main>
        </v-layout>
    </v-card>
</template>

<script>
import axios from 'axios'
import { Base64 } from 'js-base64'
export default {
    data: function () {
        return {
            ruleForm: {
                username: "Administrator",
                password: "999526",
            },
            valid: true,
            name: "",
            nameRule: [
                value => !!value || "Name can't be empty",
                value => value.length <= 20 || 'Max length 20',
            ],
            passwordRule: [
                value => !!value || "Password can't be empty",
                value => {
                    const pattern = /[A-Za-z0-9]*/
                    return pattern.test(value) || 'Only character or number'
                }
            ],
        }
    },
    // mounted() {
    //     this.ruleForm =  {
    //             username: "",
    //             password: ""
    //         }
    // },
    methods: {
        login() {
            const _this = this
            console.log(this.$refs.ruleForm.validate())
            this.$refs.ruleForm.validate().then(result => {
                console.log(result)
                if (result.valid) {
                    axios({
                        url: "http://127.0.0.1:5000/api/login",
                        method: 'post',
                        data: {},
                        headers: {
                            'username': this.ruleForm.username,
                            'password': this.ruleForm.password,
                            'authorization': 'Basic ' + Base64.encode(this.ruleForm.username + ":" + this.ruleForm.password)
                        }
                    }).then((res) => {
                        const token = res.headers['authorization']
                        console.log(res.data)
                        console.log(token)
                        _this.$store.commit('SET_TOKEN', token)
                        _this.$store.commit('SET_USERINFO', res.data.data)
                        _this.$router.push("/blogs")
                    })
                } else { console.log('error submit' + error) }
            }
            ).catch(error => console.log('error submit' + error))
        },

        reset() {
            this.$refs.ruleForm.reset()
        }
    }
}
</script>