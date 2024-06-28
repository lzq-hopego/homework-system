<script setup lang="ts">
const {setcourseTimeList,getcookie } = useCourseStore()
import axios from "axios";
const { darkMode, statusBarHeight, menuButtonBounding } = storeToRefs(useAppStore())

onLaunch(() => {
  // #ifdef MP-WEIXIN || MP-QQ
  const systemInfo = uni.getSystemInfoSync()
  // the systemInfo.theme is only support dark mode in WeChat and QQ
  darkMode.value = systemInfo?.theme === 'dark'
  statusBarHeight.value = systemInfo!.statusBarHeight || 44
  menuButtonBounding.value = uni.getMenuButtonBoundingClientRect()
  uni.onThemeChange((res: UniApp.OnThemeChangeCallbackResult) => darkMode.value = res.theme === 'dark')
  // #endif

  // #ifdef H5
  const colorScheme = window.matchMedia('(prefers-color-scheme: dark)')
  darkMode.value = colorScheme.matches
  colorScheme.addEventListener('change', (e: MediaQueryListEvent) => darkMode.value = e.matches)
  // The data is obtained from iPhone13 miniprogram but statusBarHeight, top and bottom values are subtracted from the statusBarHeight value
  statusBarHeight.value = 0
  menuButtonBounding.value = { width: 87, height: 32, left: 281, top: 4, right: 368, bottom: 36 }
  // #endif
})
onShow(() => {
})
onHide(() => {
})


const settime = async () => {
	let token=getcookie()
  	const env=import.meta.env.MODE || 'prod'
  	let url='https://zuoye-api.lizhanqi.cn:8081/api/shijian?usertoken='+token
  	if (env==='development'){
  		// console.log(11)
  		url='http://127.0.0.1/api/shijian?usertoken='+token
  	}
      const result =await  axios.get(
        url
      );
  	let time=result['data']['data']
  	setcourseTimeList(time)
    };

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
	// setStartDay(someDate)
	// setCourseList(result.data['data'] as CourseModel[])
  };

onBeforeMount(() => {
  settime()
});
</script>

