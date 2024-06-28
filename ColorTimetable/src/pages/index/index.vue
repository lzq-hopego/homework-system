<script setup lang="ts">
import type { CourseModel } from '~/stores/course'
import CourseActionSheet from '~/components/timetable/CourseActionSheet.vue'
import TimetableContent from '~/components/timetable/TimetableContent.vue'
import courses from '~/static/courses'
import axios from "axios";
import {  onMounted } from "vue";

const { customBarHeight, statusBarHeight } = useAppStore()
const { setPageConfig } = usePageStore()
const { currentWeekIndex, isStart } = storeToRefs(useCourseStore())
const { setCourseList, setStartDay,getcookie } = useCourseStore()

onShow(() => {
  setPageConfig({ showNavBar: false })
})

// setCourseList(courses as CourseModel[])

const showCourseAction = ref(false)

// set the start date
// const someDate = new Date("")
// someDate.setDate(someDate.getDate() + -1 * 7)
// setStartDay(someDate)

function handleCreateCourse() {
  uni.navigateTo({
    url: '/pages/detail/detail',
  })
}

// handle course item click
const showActionSheet = ref(false)
const clickedCourseItem = ref<CourseModel>()
function handleShowActionSheet(courseItem: CourseModel) {
  showActionSheet.value = true
  clickedCourseItem.value = courseItem
}

function handleCloseActionSheet() {
  showActionSheet.value = false
}


const setkebiao = async () => {
	let token=getcookie()
	const env=import.meta.env.MODE || 'prod'
	let url='https://zuoye-api.lizhanqi.cn:8081/api/kebiao?usertoken='+token
	if (env==='development'){
		url='http://127.0.0.1/api/kebiao?usertoken='+token
	}
    const result = await axios.get(
      url
    );
	const someDate = new Date(result.data['start-learn-time'])
	someDate.setDate(someDate.getDate() + -1 * 7)
	setStartDay(someDate)
	setCourseList(result.data['data'] as CourseModel[])
  };
  
function handleReturnHome() {
	window.location.href='/'
}
	


onMounted(() => {
  setkebiao()
});



</script>

<template>
  <UBasePage>
    <div
      class="bg-primary text-white w-full top-0 z-200 fixed font-bold"
      :style="{ height: `${customBarHeight}px` }"
    >
      <div :style="{ 'padding-top': `${statusBarHeight}px`, 'height': `${customBarHeight - statusBarHeight}px` }">
        <div class="h-full text-center px-6 relative">
          <div class="h-full text-xl left-4 i-carbon-chevron-left absolute" @click="handleReturnHome" />
          <div
            class="flex h-full mx-auto justify-center items-center inline-block text-lg"
            @click="showCourseAction = !showCourseAction"
          >
            {{ `第${currentWeekIndex + 1}周${!isStart ? '(未开学)' : ''}` }}
            <div
              class="transition-transform duration-300 i-carbon-chevron-up"
              :class="showCourseAction ? 'rotate-180' : 'rotate-0'"
            />
			<div class="h-full text-xl right-4 i-carbon-add absolute" @click="handleCreateCourse" />
          </div>
        </div>
      </div>
    </div>
    <!-- timetable main content -->
    <TimetableContent :show-course-action="showCourseAction" @course-item-click="handleShowActionSheet" />
    <!-- course card -->
    <CourseActionSheet
      :show-action-sheet="showActionSheet" :course-item="clickedCourseItem"
      @cancel="handleCloseActionSheet"
    />
  </UBasePage>
</template>

<style scoped>
</style>
