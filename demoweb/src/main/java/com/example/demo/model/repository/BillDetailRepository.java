package com.example.demo.model.repository;

import com.example.demo.model.entity.BillDetail;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BillDetailRepository extends JpaRepository<BillDetail, String> {
    List<BillDetail> findByNumberOrderByColumn(String number);
}
