<template>
  <div class="container">
    <div>
      <logo />
      <h1 class="title">
        Booklyn
      </h1>
      <h2 class="subtitle">
        My premium Nuxt.js project
      </h2>
      <div class="links">
        <a
          href="https://nuxtjs.org/"
          target="_blank"
          class="button--green"
        >Documentation</a>
        <a
          href="https://github.com/nuxt/nuxt.js"
          target="_blank"
          class="button--grey"
        >GitHub</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import Logo from '@/components/Logo.vue'

@Component({ components: { Logo } })
export default class Index extends Vue {
  @Prop()
  public greet?: string;
}
</script>

<style>

</style>
