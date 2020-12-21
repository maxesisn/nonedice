# nonedice
Dice!插件的nonebot山寨实现


> 本项目含有大量开发阶段代码，部分实现尚未完成或与原版```Dice!```插件不一致，请阅读源码后再决定是否使用

## 目前正在进行的工作
* 使kp用昵称代为PL掷骰（及其它昵称相关功能）

## 最近完成的工作
* 重写配置文件结构，防止数据丢失问题[0e49dc9](https://github.com/maxesisn/nonedice/commit/0e49dc9dcbd4a25de3d1c0cd6cba5c48fd2c894e)


## 使用说明
在```run.py```同级目录执行
```shell
git submodule add https://github.com/maxesisn/nonedice.git hoshino/modules/nonedice
```

并在```__bot__.py```中添加插件名称即可

- 虽然插件名是nonedice，但是本插件需要[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)框架以实现部分功能（后续可能会迁移到nonebot2）

- 请禁用```HoshinoBot```的```dice```插件以避免冲突

## 功能列表
> 现在的感觉够用了！没人催就先摸了！
- [x] Help命令
- [x] 基础掷骰
- [x] 复杂掷骰表达式
- [x] COC判定掷骰
- [x] COC人物卡
- [ ] COC多人物卡
- [ ] COC跨人物卡检定
- [x] COC表达式人物卡录入
- [ ] COC成长检定
- [x] COC人物卡生成
- [x] COC检定房规设定
- [x] COC理智检定
- [x] COC疯狂列表
- [ ] Keep掷骰
- [ ] DND人物卡生成
- [ ] DND先攻
- [ ] Rules规则查询
- [x] Jrrp今日人品
- [ ] Fudge骰
- [ ] Ww骰池
- [ ] Dx骰
- [ ] Name/nnn随机名称生成
- [x] Set默认骰设定
- [ ] 各模块开启以及关闭

## 大饼列表
> 能不能完成看缘分
- [ ] 脱离HoshinoBot框架
- [ ] 导入Excel人物卡
- [ ] 输出图片人物卡
- [ ] 背景故事生成