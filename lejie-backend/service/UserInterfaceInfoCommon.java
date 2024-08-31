import com.baomidou.mybatisplus.service.IService;
import model.entity.User;
import model.entity.UserInterfaceInfo;


public interface UserInterfaceInfoService extends IService<UserInterfaceInfo> {
    void validUserInterfaceInfo(UserInterfaceInfo userInterfaceInfo, boolean add)

    User getInvokeUser(String accessKey, String secretKey)

    InterfaceInfo getInterfaceInfo(String path, String method)

    /**
     * 调用接口统计
     */
    boolean invokeCount(long interfaceInfoId, long userId);
}

// maven 将 common 包打包到本地提供给其他项目使用
