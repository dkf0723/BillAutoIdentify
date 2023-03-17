package com.example.demo.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "發票主檔" )
public class Bill {
    @Id
    @Column(name = "發票號碼", length = 18, nullable = false)
    private String billNumber;

    @Column(name = "二聯三聯", length = 18)
    private String billType;

    @Column(name = "年份月份", length = 18 )
    private String yearMonth;

    @Column(name = "日期")
    private LocalDateTime dateTime;

    @Column(name = "統一編號", length = 18)
    private String taxIdNumber;

    @Column(name = "買受人", length = 30)
    private String buyer;

    @Column(name = "地址", length = 50)
    private String address;

    @Column(name = "合計")
    private Integer total;

    @Column(name = "稅別", length = 18)
    private String taxType;

    @Column(name = "稅額")
    private Integer taxNumber;

    @Column(name = "總計")
    private Integer totalAddTax;

    @Column(name = "中文總計", length = 18)
    private String chineseTotalAddTax;

    @Column(name = "匯入日期", length = 18)
    private String includeDateTime;

    @Column(name = "修改者帳號", length = 18)
    private String modifyUserId;

    @Column(name = "檢核正確否", length = 18)
    private String check;

    @Column(name = "掃描檔連結", length = 18)
    private String picture;

    @Column(name = "匯入人員", length = 18)
    private String includeSource;
}
