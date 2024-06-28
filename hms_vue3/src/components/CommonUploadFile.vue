<template>
  <!-- 注意这里的 action="#"，和:auto-upload="false"，如果:auto-upload="true"，由于el-upload的change事件，上传和上传成功都会回调，这里
    将其设置为false，不自动上传，不然会重复请求。 :show-file-list="true"是否展示文件列表，如果不需要就设置为false就可以了，
  v-model:file-list="fileList"文件列表数组，具体看官网就行了, accept=".mp4"接收的文件类型，这里只接受mp4，可以填多个如：accept=".mp4, mp3, .jpg" -->
  <el-upload
    class="upload-demo"
    action="#"
    drag
    :auto-upload="false"
    :show-file-list="true"
    v-model:file-list="fileList"
    :on-change="handleChange"
    :on-remove="handleRemove"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">拖拽文件到这里或者<em>点击上传</em></div>
    <template #tip>
      <!-- <div class="el-upload__tip">
          jpg/png files with a size less than 500kb
        </div> -->
    </template>
  </el-upload>
  <el-row>
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="name" label="名字" />
      <el-table-column prop="percentage" label="进度">
        <template #default="scope">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="scope.row.percentage"
          />
        </template>
      </el-table-column>
      <el-table-column prop="percentage" label="操作">
        <template #default="scope">
          <el-button
            type="primary"
            @click="handleRemoveUploadFileList(scope.row)"
            >删除</el-button
          >
          <!-- <el-button type="primary" @click="handlePreviewUploadFileList(scope.row)">预览</el-button> -->
        </template>
      </el-table-column>
    </el-table>
  </el-row>
  <el-row>
    <!-- 这个要设置宽度，否则有可能显示不出来 -->
    <!-- <el-progress style="width: 100%" :text-inside="true" :stroke-width="26" :percentage="percentage" /> -->
  </el-row>
  <!-- <el-dialog v-model="dialogTableVisible" title="预览视频" @close="handleClose">
      <video v-if="dialogTableVisible" width="800" height="600" controls loop id="video-play">
        <source :src="videoPath" type="video/mp4">
        您的浏览器不支持 video 标签。
      </video>
    </el-dialog> -->
</template>
  
  <script setup >
import axios from "axios";
import { UploadFilled } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { ref, getCurrentInstance } from "vue";
// import CryptoJS from 'crypto-js';
import SparkMD5 from "spark-md5";
import { useStore } from "vuex";

const { proxy } = getCurrentInstance();
const store = useStore();
// store.commit("AlterFileHash");


const tableData = ref([]);
// 文件列表
const fileList = ref([]);
// 分块大小1mb
const chunkSize = 1024 * 1024;
/**
 * 将分块文件上传至服务器
 * @param file 上传的分块文件
 * @param chunkNumber 当前是第几块
 * @param chunkTotal 文件分块的总数
 * @param fileName 文件名称
 */
const uploadFileToServer = async (
  file,
  chunkNumber,
  chunkTotal,
  fileName,
  FileHash
) => {
  const form = new FormData();
  // 这里的data是文件
  form.append("file", file);
  form.append("chunkNumber", chunkNumber);
  form.append("chunkTotal", chunkTotal);
  form.append("fileName", fileName);
  form.append("FileHash", FileHash);
  // const result = await axios.post("http://127.0.0.1/api/zy/upload", form)

  const result = await proxy.$api.postzyupload(form);

  return result;
};

/**
 * 合并文件
 * @param chunkTotal 文件分块的总数量
 * @param fileName 文件名称
 */
const mergeFiles = async (chunkTotal, fileName, FileHash, ClassTaskToken,randomNum) => {
  const result = await proxy.$api.mergeFileszyupload({
    chunkTotal: chunkTotal,
    fileName: fileName,
    FileHash: FileHash,
    ClassTaskToken: ClassTaskToken,
    randomNum:randomNum,
  });
  ElMessage.success("上传成功！");
  return result;
};

/**
 * 根据文件名删除文件
 * @param fileName 文件名
 */
const deleteFileByFileName = async (fileName) => {
  // const result = await axios.get(
  //   `http://127.0.0.1/api/zy/upload?fileName=${fileName}`
  // );
  // // 这个result.data这个不多说了，axios相关的，不懂的console.log(result)就知道了
  // console.log(result.data);
};

/**
 * el-upload内置的change函数，文件上传或者上传成功时的回调，不过这里因为
 * :auto-upload="false"的缘故，上床成功的回调不会执行
 * @param uploadFile el-upload当前上传的文件对象
 * @param uploadFiles el-upload上传的文件列表
 */

const hash = ref(null);

const handleChange = async (uploadFile, uploadFiles) => {
  // v-model:file-list="fileList" 就是这里的uploadFiles。这两个文件列表是一样的，多以在删除的时候，从fileList清除某一项，uploadFiles这里也会清除的
  // 这个el-upload 已经实现了的

  // 作业的token
  const ClassTaskToken = store.state.ClassTaskToken;
  const username=store.state.username
  let randomNum = Math.random();
  // console.log(randomNum)

  const FileHash = SparkMD5.hash(ClassTaskToken+username+randomNum);

  const fileName=uploadFile.raw.name
  
  //   const FileHash=hash._rawValue

  tableData.value.push({ ...uploadFile });
  const index = tableData.value.findIndex(
    (item) => item.uid === uploadFile.uid
  );

  const fileSize = uploadFile.size || 0;

  let chunkTotals = Math.ceil(fileSize / chunkSize);
  if (chunkTotals > 0) {
    for (
      let chunkNumber = 0, start = 0;
      chunkNumber < chunkTotals;
      chunkNumber++, start += chunkSize
    ) {
      let end = Math.min(fileSize, start + chunkSize);
      // uploadFile.raw这个是element plus 中 el-upload的自己上传的文件就放在这个raw里面，可以console.log(uploadFile)看一下
      // 加 ？是因为ts语法提示“uploadFile.raw”可能为“未定义”，加了这个就不过有报错了
      const files = uploadFile.raw?.slice(start, end);
      const result = await uploadFileToServer(
        files,
        chunkNumber + 1,
        chunkTotals,
        fileName,
        FileHash
      );
      // console.log(result)
      const percents = parseFloat(result.progress.replace("%", ""));
      uploadFile.percentage = percents;
      tableData.value[index].percentage = percents;
      // percentage.value = percents
      // console.log(result.data)
    }
    // 这里可以tableData.value[index].percentage先判断一下进度是否100%了，然后再合并，防止只上传了一半中途出现问题了也合并
    const reader = new FileReader();
    var Spark=new SparkMD5.ArrayBuffer()
      reader.onload =async(e) => {
        const binary = e.target.result;
        Spark.append(binary)
        hash.value=Spark.end()
        const videoUrl = await mergeFiles(
          chunkTotals,
          fileName,
          hash.value,
          ClassTaskToken,
          randomNum
        );
        tableData.value[index].url = videoUrl;
      };
    reader.readAsArrayBuffer(uploadFile.raw);
    
  }

  // console.log(uploadFiles)
};

/**
 * 从el-upload封装的文件列表中删除文件
 * // el-upload的（内置方法），点击el-upload默认的文件展示以列表的 X 那个图标时，会移除文件，并从文件列表中去掉
 * @param uploadFile el-upload当前删除点击的文件
 * @param uploadFiles el-upload的文件列表
 */
const handleRemove = async (uploadFile, uploadFiles) => {
  // 这个删除表格tableData中的列表数据
  const index2 = tableData.value.findIndex(
    (item2) => item2.uid === uploadFile.uid
  );
  if (index2 !== -1) {
    tableData.value.splice(index2, 1);
  }
  await deleteFileByFileName(uploadFile.name);
  // handleRemove内置的删除文件方法，
  // 这里的uploadFiles跟绑定的v-model:file-list="fileList"可以看成是同一个数组，这两个数组的数据是一样的，从这两个数组中删除或者移除任何一个数据，
  // 另外一个数据也会跟着变化的，这个element plus已经实现了
  // console.log(uploadFiles);
};

/**
 * 自定义的表格删除的方法
 * @param file 表格某一行的数据
 */
const handleRemoveUploadFileList = async (file) => {
  const index = fileList.value.findIndex((item) => item.uid === file.uid);
  if (index !== -1) {
    fileList.value.splice(index, 1);
  }
  const index2 = tableData.value.findIndex((item2) => item2.uid === file.uid);
  if (index2 !== -1) {
    tableData.value.splice(index2, 1);
  }

  // 删除磁盘中的文件
  await deleteFileByFileName(file.name);
};
</script>
  
  <style scoped></style>
  