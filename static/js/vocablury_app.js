
    const { createApp } = Vue;

            createApp({
                delimiters: ['[[', ']]'] ,
                data() {
                    return {
                   maxviewWords :60 ,
                    currentIndex: 0,
                    list_tense :['past simple' , 'past continous' , 'past perfect', 'present simple' , 'present continous' , 'present perfect' , 'future simple', 'future continous' , 'future perfect'] ,
                    verbs:[] ,
                    verbid_:[] ,
                    verbEnglish_: [],
                    verbSentence_: [],
                    vocabluryCount_: [],
                    verbpath_: [],
                    verbRate_: [],
                    verbStat_: [],
                    verbType_: [],
                    verbname_: [],
                    verbNote_: [],
                    verbLangArabic_:[],
                    verbLangRusian_: [],
                    verbLangspanish_: [],
                    verbLangDeutsch_: [],
                    verbLangChain_: [] ,

                    }
                } ,
                 // end data

                methods: {
                nextWord() {
                    if (this.currentIndex < this.maxviewWords - 1) {
                        this.currentIndex++;
                    } else {
                        // Loop back to the first word
                        this.currentIndex = 0;
                    }
                },
                prevWord() {
                    if (this.currentIndex > 0) {
                        this.currentIndex--;
                    } else {
                        // Go to the last word
                        this.currentIndex = this.maxviewWords - 1;
                    }
                },
                markReview(){
                alert(`تم تعديل  ${this.verbs.length} مفردة بنجاح`);
                Vocablury_main =this.verbid_[this.currentIndex];
                rant = 2 ;
                fetch('http://127.0.0.1:8000/api/update_user_Vocablury/update/${Vocablury_main}/${rant}/')
                .then(res => {
                        if (!res.ok) {
                            throw new Error(`خطأ في الخادم: ${res.status}`);
                        }
                        return res.json();
                    })
                .catch(error => {
                        console.error("فشل في جلب البيانات:", error);
                        alert('خطأ في تحميل البيانات: ' + error.message);
                    });

                },
            } ,
             // end Mothed

               mounted() {
                    fetch('http://127.0.0.1:8000/api/api_vocablury_filter/')
                    .then(res => {
                        if (!res.ok) {
                            throw new Error(`خطأ في الخادم: ${res.status}`);
                        }
                        return res.json();
                    })
                    .then(data => {
                        if (!data || !data.vocablury) {
                            throw new Error('بيانات غير صالحة');
                        }

                        this.verbs = data.vocablury;

                        // استخدام console.log بدلاً من alert للكائنات الكبيرة
                        console.log('البيانات المستلمة:', this.verbs);

                        // تفريغ المصفوفات قبل التعبئة
                        this.verbid_ = [];
                        this.verbEnglish_ = [];
                        this.verbname_ = [];
                        this.verbLangArabic_ = [];

                        this.verbs.forEach((element, index) => {
                            this.verbid_.push(element.id || index);
                            this.verbEnglish_.push(element.vocablury_en || '');
                            this.vocabluryCount_.push(element.vocablury_count || '');
                            this.verbname_.push(element.vocablury_type || '');
                            this.verbLangArabic_.push(element.vocablury_en_id[0]['vocablury_mean'] || '');

                        });

                        // عرض رسالة نجاح مختصرة
                        alert(`تم تحميل ${this.verbs.length} مفردة بنجاح`);
                    })
                    .catch(error => {
                        console.error("فشل في جلب البيانات:", error);
                        alert('خطأ في تحميل البيانات: ' + error.message);
                    });
                } ,
            }).mount('#app');
            //app.config.compilerOptions.delimiters = ['[[', ']]'];


